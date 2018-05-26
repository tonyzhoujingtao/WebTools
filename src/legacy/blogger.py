#!/usr/bin/python

# This file demonstrates how to use the Google Data API's Python client library
# to interface with the Blogger service.  There are examples for the following
# operations:
#
# * Retrieving the list of all the user's blogs
# * Retrieving all posts on a single blog
# * Performing a date-range query for posts on a blog
# * Creating draft posts and publishing posts
# * Updating posts
# * Retrieving comments
# * Creating comments
# * Deleting comments
# * Deleting posts


__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

import gdata.blogger.client, atom.data

class BloggerService:
    def __init__(self):
        """Creates a GDataService and provides ClientLogin auth details to it.
        The email and password are required arguments for ClientLogin.  The
        'source' defined below is an arbitrary string, but should be used to
        reference your name or the name of your organization, the app name and
        version, with '-' between each of the three values."""
    
        # Authenticate using ClientLogin, AuthSub, or OAuth.
        self.client = gdata.blogger.client.BloggerClient()
#         gdata.sample_util.authorize_client(
#             self.client, service='blogger', source='BloggerService-1.0',
#             scopes=['http://www.blogger.com/feeds/'])
        
        self.client.client_login('tony.zjt.test@gmail.com', 'Vathsa79', source='BloggerService-1.0', service='blogger')
    
        # Get the blog ID for the first blog.
        feed = self.client.get_blogs()
        self.blog_id = feed.entry[0].get_blog_id()

    def print_user_blog_titles(self):
        """Prints a list of all the user's blogs."""
        
        feed = self.client.get_blogs()
        
        print feed.title.text
        for entry in feed.entry:
            print "\t" + entry.title.text
        print

    def create_post(self, title, content, is_draft):
        """This method creates a new post on a blog.  The new post can be stored as
        a draft or published based on the value of the is_draft parameter.  The
        method creates an GDataEntry for the new post using the title, content,
        author_name and is_draft parameters.  With is_draft, True saves the post as
        a draft, while False publishes the post.  Then it uses the given
        GDataService to insert the new post.  If the insertion is successful, the
        added post (GDataEntry) will be returned.
        """
        print "Create post with title as: %s" % title
        return self.client.add_post(self.blog_id, title, content, draft=is_draft)

    def print_all_posts(self):
        """This method displays the titles of all the posts in a blog.  First it
        requests the posts feed for the blogs and then it prints the results.
        """
        # Request the feed.
        feed = self.client.get_posts(self.blog_id)
        
        # Print the results.
        print feed.title.text
        for entry in feed.entry:
            if not entry.title.text:
                print "\tNo Title"
            else:
                print "\t" + entry.title.text.encode('utf-8')
        print
    
    def print_posts_in_date_range(self, start_time, end_time):
        """This method displays the title and modification time for any posts that
        have been created or updated in the period between the start_time and
        end_time parameters.  The method creates the query, submits it to the
        GDataService, and then displays the results.
        
        Note that while the start_time is inclusive, the end_time is exclusive, so
        specifying an end_time of '2007-07-01' will include those posts up until
        2007-6-30 11:59:59PM.
        
        The start_time specifies the beginning of the search period (inclusive),
        while end_time specifies the end of the search period (exclusive).
        """
        
        # Create query and submit a request.
        query = gdata.blogger.client.Query(updated_min=start_time,
                                           updated_max=end_time,
                                           order_by='updated')
        print query.updated_min
        print query.order_by
        feed = self.client.get_posts(self.blog_id, query=query)
        
        # Print the results.
        print feed.title.text + " posts between " + start_time + " and " + end_time
        print feed.title.text
        for entry in feed.entry:
            if not entry.title.text:
                print "\tNo Title"
            else:
                print "\t" + entry.title.text
        print

    def update_post_title(self, entry_to_update, new_title):
        """This method updates the title of the given post.  The GDataEntry object
        is updated with the new title, then a request is sent to the GDataService.
        If the insertion is successful, the updated post will be returned.
        
        Note that other characteristics of the post can also be modified by
        updating the values of the entry object before submitting the request.
        
        The entry_to_update is a GDatEntry containing the post to update.
        The new_title is the text to use for the post's new title.  Returns: a
        GDataEntry containing the newly-updated post.
        """
        
        # Set the new title in the Entry object
        entry_to_update.title = atom.data.Title(type='xhtml', text=new_title)
        return self.client.update(entry_to_update)

    def create_comment(self, post_id, comment_text):
        """This method adds a comment to the specified post.  First the comment
        feed's URI is built using the given post ID.  Then a GDataEntry is created
        for the comment and submitted to the GDataService.  The post_id is the ID
        of the post on which to post comments.  The comment_text is the text of the
        comment to store.  Returns: an entry containing the newly-created comment
        
        NOTE: This functionality is not officially supported yet.
        """
        return self.client.add_comment(self.blog_id, post_id, comment_text)

    def print_all_comments(self, post_id):
        """This method displays all the comments for the given post.  First the
        comment feed's URI is built using the given post ID.  Then the method
        requests the comments feed and displays the results.  Takes the post_id
        of the post on which to view comments. 
        """
        
        feed = self.client.get_post_comments(self.blog_id, post_id)
        
        # Display the results
        print feed.title.text
        for entry in feed.entry:
            print "\t" + entry.title.text
            print "\t" + entry.updated.text
        print

    def delete_comment(self, comment_entry):
        """This method removes the comment specified by the given edit_link_href, the
        URI for editing the comment.
        """
        self.client.delete(comment_entry)

    def delete_post(self, post_entry):
        """This method removes the post specified by the given edit_link_href, the
        URI for editing the post.
        """
        print "Deleting post: %s .." % post_entry
        self.client.delete(post_entry)
        print "Deleting post: %s .. OK" % post_entry

    def delete_all_posts(self):
        feed = self.client.get_posts(self.blog_id)
        
        for entry in feed.entry:
            self.delete_post(entry)
              
    def demo(self):
        """Runs each of the example methods defined above, demonstrating how to
        interface with the Blogger service.
        """
        # Demonstrate retrieving a list of the user's blogs.
        self.print_user_blog_titles()
        
        # Demonstrate how to create a draft post.
        draft_post = self.create_post('YY is a cute',
          "<p>I love YY's new hair style and perfume.</p>",
          True)
        print 'Successfully created draft post: "' + draft_post.title.text + '".\n'
        
        # Delete the draft blog post.
        self.client.delete(draft_post)
        
        # Demonstrate how to publish a public post.
        public_post = self.create_post("ZJ's is also cute",
          "<p>ZJ likes to read.</p>",
          False)
        print "Successfully created public post: \"" + public_post.title.text + "\".\n"
        
        # Demonstrate various feed queries.
        print "Now listing all posts."
        self.print_all_posts()
        print "Now listing all posts between 2007-04-04 and 2007-04-23."
        self.print_posts_in_date_range("2007-04-04", "2007-04-23")
        
        # Demonstrate updating a post's title.
        print "Now updating the title of the post we just created:"
        public_post = self.update_post_title(public_post, 'YY is cute')
        print "Successfully changed the post's title to \"" + public_post.title.text + "\".\n"
        
        # Demonstrate how to retrieve the comments for a post.
        # Get the post ID and build the comments feed URI for the specified post
        post_id = public_post.get_post_id()
        
        print "Now posting a comment on the post titled: \"" + public_post.title.text + "\"."
        comment = self.create_comment(post_id, "Did you see any sharks?")
        print "Successfully posted \"" + comment.content.text + "\" on the post titled: \"" + public_post.title.text + "\".\n"
        
        print "Now printing all comments"
        self.print_all_comments(post_id)
        
        # Delete the comment we just posted
        print "Now deleting the comment we just posted"
        self.delete_comment(comment)
        print "Successfully deleted comment." 
        self.print_all_comments(post_id)
        
        # Demonstrate deleting posts.
        print "Now deleting the post titled: \"" + public_post.title.text + "\"."
        self.delete_post(public_post)
        print "Successfully deleted post." 
        self.print_all_posts()
        

def main():
    bloggerService = BloggerService()
    bloggerService.demo()


if __name__ == '__main__':
    main()
