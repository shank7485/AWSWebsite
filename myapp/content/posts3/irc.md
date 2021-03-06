title: Setting up IRC client
date: 8/10/2016
details: Simple tutorial to setup Weechat IRC client.
post_no: 2

## **IRC (Internet Rely Chat)**

Ever since I wanted to contribute to an open-source project, I was told on online forums to contact the specific IRC channels to ask questions and start contributing. That's fine. I'll do that. But I never understood what was IRC.
### **So what's IRC?**
Wikipedia quotes 'Internet Relay Chat Protocol (IRCP) is an application layer protocol that facilitates communication in the form of text. The chat process works on a client/server networking model.'
In plain works, it's a chat app. But a chat app which you can use on a command line (GUI is also available. Don't worry :) ) 
### **Why and Who uses IRC?**
Suppose you want to send some information to someone or a group of people, you can do it through IRC. You can create 'chatrooms' on the go, send messages etc. It's way easier to communicate. But the main advantage is all this can be done on the command line. This was/is is very useful when you are doing development and you are SSH'd into a remote server and have only the command line at your disposal. You can login into your account and start sending messages all through the command line. From what I see, most open source people use IRC. Why? I guess it goes back to age of Linux when there were no fancy chat apps like Slack or WhatsApp to communicate.
### **Setup**
* Command Line: I use [Weechat](https://help.ubuntu.com/community/WeeChat) (not wechat app) as my command line IRC client. To setup, follow the command below on a Ubuntu instance (Debian stuff).
    * Add repo, get latest repo list, install.

        ```sudo add-apt-repository -y ppa:nesthib/weechat-stable```

        ```sudo apt-get update```

        ```sudo apt-get install weechat -y```

    * Fire up Weechat.

        ```weechat```

    * You can start using it right away. But to save your channels
    (subscriptions),     you need register your nick name. Nick name is basically like username used in      apps. Choose user name by running the below command;

        ```/nick <username>```

    * Now we need to register this with a server. In my case I will use Freenode.       Freenode is like the server side guy who maintains your account. 

        ```/connect chat.freenode.net```

    * Register using;

        ```/msg NickServ REGISTER <password> <youremail@example.com>```

    * You will get an email from Freenode with a command to run. It should look something like this 

        ```/msg NickServ VERIFY REGISTER <usernamae> <random stuff>```

    * Once that is done, you are now a registered user. To login, you do this;

        ```/nick <username>```

        ```/msg NickServ IDENTIFY <username> <password>```

That's it. You are now logged in. You can start conversing by running the following commands;

* To talk to another IRC username ;

    ```/query <other's username>```

* To join a channel ;

    ```/join #<channel name>```

    Example: ```/join #linux``` or ```/join #openstack```. 
    If the channel is not present, you can create with the same command as above.

* To scroll up and down the chat use page up and page down.

* To close from chat bot ```/close```

* To quit weechat ```/exit```

* GUI: Setting up commands are same as command line in IRC. I use Limechat for Mac and HexChat for Windows.

### **Final words**
This simple tutorial is by no means a holistic view of what all weechat or IRC can do. But it's a good entry point to understand. To know more visit [https://weechat.org/files/doc/devel/weechat_user.en.html](https://weechat.org/files/doc/devel/weechat_user.en.html)

**Also, you can contact me on IRC by ```/query sshank``` **
