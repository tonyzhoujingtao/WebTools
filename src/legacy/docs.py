'''
Created on 2013-4-28

@author: Tony
'''

from gdata.docs.service import DocsService

def main():
    client = DocsService()
    client.ClientLogin('tony.zjt.test@gmail.com', 'Vathsa79')
    documents_feed = client.GetDocumentListFeed()
    for document_entry in documents_feed.entry:
        print document_entry.title.text

if __name__ == '__main__':
    main()
