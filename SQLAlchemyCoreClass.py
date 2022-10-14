from sqlalchemy import Table, func, literal_column
from sqlalchemy.sql import insert, select, update
from ConnectDB import ConnectDB
from sqlalchemy.sql import and_


class CoreFunctions:
    def __init__(self, database, tablename, schema='in_use'):
        obj = ConnectDB(database)
        self.tablename = tablename
        self.engine = obj.get_dbengine()
        self.schema = schema
        self.session = obj.get_session()
        self.metadata = obj.get_metadata()
        self.table_object = self.table_exists()
        self.table_columns = [i.name for i in self.table_object.columns]

    def _get_table_object(self):
        return Table(self.tablename, self.metadata, autoload=True, autoload_with=self.engine)

    def _verify_payload(self, payload):
        if type(payload) == list and payload:
            keys = set(payload[0].keys())
            extra_columns = keys - set(self.table_columns)
            if extra_columns:
                raise Exception('Invalid payload: payload has additional columns than expected in the table')

    def table_exists(self):
        if self.engine.has_table(self.tablename):
            return self._get_table_object()
        else:
            raise Exception('Table {} doesn not exists'.format(self.tablename))

    def get_column_names_and_dtypes(self):
        return {c.name: c.type.python_type for c in self.table_object.columns}

    def get_mandatory_column_names(self):
        return {c.name: not c.nullable for c in self.table_object.columns}

    def select_all(self, order_by=None):
        select_obj = select([self.table_object]).order_by(order_by) if order_by else select([self.table_object])
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_where(self, column_name, column_value):
        select_obj = select([self.table_object]).where(self.table_object.c[column_name] == column_value)
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_where_multiple(self, payload):
        where_condition = [self.table_object.c[column_name] == column_value
                           for column_name, column_value in payload.items()]
        select_obj = select([self.table_object]).where(and_(*where_condition))
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_where_multiple_paginate(self, payload, maximum, offset, cols_to_exclude=[]):
        where_condition = [self.table_object.c[column_name] == column_value
                           for column_name, column_value in payload.items()]
        select_obj = select([self.table_object]).where(and_(*where_condition)).limit(maximum).offset(offset)
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict([(x, y) for x, y in zip(self.table_columns, result) if x not in cols_to_exclude])

    def select_in(self, column_name, column_values):
        select_obj = select([self.table_object]).where(self.table_object.c[column_name].in_(column_values))
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_in_where(self, where_payload, in_payload):
        where_condition = [self.table_object.c[column_name] == column_value
                           for column_name, column_value in where_payload.items()]
        in_payload = self.table_object.c[in_payload["in_column_name"]].in_(in_payload["in_column_value"])
        select_obj = select([self.table_object]).where(and_(in_payload, *where_condition))
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_columns_using_in(self, select_columns, in_payload, alias_names=None):
        in_payload = self.table_object.c[in_payload["in_column_name"]].in_(in_payload["in_column_value"])
        select_obj = select([self.table_object.c[i] for i in select_columns]).where(in_payload)
        rs = self.session.execute(select_obj)
        table_columns = alias_names if alias_names else self.table_columns
        for result in rs:
            yield dict(zip(table_columns, result))

    def select_column(self, columnname):
        if type(columnname) != list:
            columnname = [columnname]
        select_obj = select([self.table_object.c[i] for i in columnname])
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(columnname, result))

    def select_column_where(self, where_payload, select_columns):
        select_columns = [select_columns] if type(select_columns) != list else select_columns
        where_condition = [self.table_object.c[column_name] == column_value
                           for column_name, column_value in where_payload.items()]
        select_obj = select([self.table_object.c[i] for i in select_columns]).where(and_(*where_condition))
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(select_columns, result))

    def select_where_using_like(self, columnname, query):
        like_object = [self.table_object.c[columnname].ilike("%{}%".format(search_query)) for search_query in
                       query.split()]
        select_obj = select([self.table_object]).where(and_(*like_object))
        rs = self.session.execute(select_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def insert(self, payload):
        self._verify_payload(payload)
        insert_obj = insert(self.table_object)
        insert_obj = insert_obj.values(payload)
        self.session.execute(insert_obj)

    def insert_object(self, payload):
        self._verify_payload(payload)
        insert_obj = insert(self.table_object)
        insert_obj = insert_obj.values(payload)
        self.session.execute(insert_obj)
        self.session.commit()

    def insert_returning(self, payload):
        self._verify_payload(payload)
        insert_obj = insert(self.table_object)
        insert_obj = insert_obj.values(payload).returning(literal_column('*'))
        rs = self.session.execute(insert_obj)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def update_object(self, where_column_name, where_column_value, payload):
        stmt = update(self.table_object).where(self.table_object.c[where_column_name] == where_column_value).values(
            payload)
        self.session.execute(stmt)

    def update_returning(self, where_column_name, where_column_value, payload):
        stmt = update(self.table_object).where(self.table_object.c[where_column_name] == where_column_value).values(
            payload).returning(literal_column('*'))
        rs = self.session.execute(stmt)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def update_returning_v2(self, where_payload, payload):
        where_condition = [self.table_object.c[column_name] == column_value
                           for column_name, column_value in where_payload.items()]
        stmt = update(self.table_object).where(and_(*where_condition)).values(
            payload).returning(literal_column('*'))
        rs = self.session.execute(stmt)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def update_returning_using_in(self, in_payload, update_payload):
        in_condition = self.table_object.c[in_payload["in_column_name"]].in_(in_payload["in_column_value"])
        stmt = update(self.table_object).where(in_condition).values(
            update_payload).returning(literal_column('*'))
        rs = self.session.execute(stmt)
        for result in rs:
            yield dict(zip(self.table_columns, result))

    def select_groupby(self, select_column, count_column='id', label=None, alias=None):
        select_stmt = [self.table_object.c[c] for c in select_column] + [func.count(self.table_object.c[count_column].label(label))]
        select_obj = select(select_stmt).group_by(*select_column)
        rs = self.session.execute(select_obj)
        table_columns = alias if alias else select_column
        for result in rs:
            yield dict(zip(table_columns, result))

    @staticmethod
    def core_to_dict(result_set, date_format=None):
        data = {}
        for col in result_set:
            result_set[col]
            if isinstance(result_set[col], datetime.date):
                if date_format:
                    data[col] = result_set[col].strftime(date_format)
                else:
                    data[col] = str(result_set[col])
            elif isinstance(result_set[col], datetime.time):
                data[col] = str(result_set[col])
            elif isinstance(result_set[col], Decimal):
                data[col] = round(float(result_set[col]))
            else:
                data[col] = result_set[col]
        return data

    def execute_query(self, query, alias_names):
        rs = self.session.execute(query)
        for result in rs:
            yield dict(zip(alias_names, result))

    def session_commit(self):
        return self.session.commit()

if __name__ == "__main__":
    obj = CoreFunctions("movesoutput")
    print(obj.table_columns)
