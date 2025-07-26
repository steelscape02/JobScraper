
from scraper.store import Store
from scraper.job import Job

def sync(new_list : list[dict[str,str]], existing_items: Store):


    # add and update
    for new_item in new_list:
        found_new = False
        for old_item in existing_items.fireDB.stream():
            if new_item.get('url') == old_item.url: #url is uuid
                found_new = True
                #TODO: Reimp update
                adder = Job(new_item.get('url'))
                adder.from_dict(new_item)
                existing_items.update(adder)
                break
        if not found_new:
            adder = Job(new_item.get('url'))
            adder.from_dict(new_item)
            existing_items.update(adder)

    # remove
    for old_item in existing_items.fireDB.stream():
        found_old = False
        for new_item in new_list:
            if old_item.url == new_item.get('url'): #url is uuid
                found_old = True
                break
        
        if not found_old:
            existing_items.remove(old_item.url)

