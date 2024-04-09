import os
import shutil


def delete(filenames, list):
    for r in list:
        if r['title'] not in filenames.split(','):
            continue

        if not os.path.exists(r['filepath']):
            print(f"Not Exists: {r['filepath']}")
            continue

        print(f"Delete: {r['filepath']}")
        if os.path.isdir(r['filepath']):
            shutil.rmtree(r['filepath'])
        else:
            os.remove(r['filepath'])
            if (os.path.exists(r['filepath'] + '.sha256')):
                try:
                    os.remove(r['filepath'] + '.sha256')
                except:
                    pass
            if (os.path.exists(os.path.splitext(r['filepath'])[0] + '.yaml')):
                try:
                    os.remove(os.path.splitext(r['filepath'])[0] + '.yaml')
                except:
                    pass
    print("Delete Done!")
