from app.database.mysql_decorator import conn_msql


# to get who get special permisson
@conn_msql
def authorized_permission(query_obj, **kwargs):
    sql = """
    select distinct acl.acl, aa.menu as module
    from ous,
    ous_acl_mapping,
    acl, 
    menu,
    menu aa
    where 
    ous.ou = ous_acl_mapping.ou 
    and ous_acl_mapping.acl = acl.id 
    and acl.module = aa.menu
    and menu.parent = aa.id
    and ous_acl_mapping.status = 1
    and ous.ou in (%s)
    """ % (",".join(["%(ou" + str(i) + ")s" for i in range(len(kwargs['ou']))]))
    return sql


