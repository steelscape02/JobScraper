from firebase_admin.firestore import firestore

def sync(db : firestore.CollectionReference, new_list : list[dict[str,str]]):


    # add and update
    for new_item in new_list:
        found_new = False
        for old_item in db.stream():
            if new_item.get('url') == old_item.get('url'): #url is uuid
                found_new = True
                old_item.update(new_item) # Updates existing old item in temp with new values
                db.document(new_item.get('url')).update(new_item)  # Assuming url is unique and used as document ID
                break
        if not found_new:
            db.document(new_item.get('url')).set(new_item)

    # remove
    for old_item in db.stream():
        found_old = False
        for new_item in new_list:
            if old_item.get('url') == new_item.get('url'): #url is uuid
                found_old = True
                break
        
        if not found_old:
            db.document(old_item.get('url')).delete()  # Delete from Firestore

