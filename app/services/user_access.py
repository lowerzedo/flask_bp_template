from app.models.user_access import authorized_permission

def get_user_access(kwargs,status):
    
    ouList = kwargs["memberOf"] if status == 'microsoft' else []
    aclList = []

    if status == 'cas':
        member_of = kwargs['cas:memberOf'] if 'cas:memberOf' in kwargs else kwargs['memberOf']
        for m in member_of:
            removeCn = m[3:]
            ouList.append(removeCn.split(',')[0])

    query_obj = {}
    for i in range(len(ouList)):
        query_obj['ou' + str(i)] = ouList[i]

    acl = authorized_permission(query_obj, ou=ouList)

    for a in acl:
        aclList.append(a['acl'])

    results = { 
        "ACL": aclList
    }

    return results