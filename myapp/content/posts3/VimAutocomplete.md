title: Code Completion in Vim Editor using YouCompleteMe and Vundle
date: 10/2/2016
details: Tutorial to setup code completeion in Vim.
post_no: 3

Get code completion for Python like an IDE in the terminal using Vim editor with
YouCompleteMe and Vungle plugin. Similar to

<div class="text-center">
<img align="center" src="https://raw.githubusercontent.com/shank7485/Blog_Files/master/0OP4ood.gif" width="500" height="400" />
</div>


### **This is for Ubuntu Linux (Debian) based OSes.**

### **Steps to be followed:**

* Update to latest Vim. This is done as Vim version greater than 7.41 isn't available in Apt-get of Ubuntu Linux.

    ```sudo add-apt-repository ppa:pkg-vim/vim-daily```


    ```sudo apt-get update```

    ```sudo apt-get install vim```

    ```dpkg -s vim | grep 'Version' #should be greater than 7.41```

    ```touch ~/.vimrc```

* Get Vundle.

    ```git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim```

* Add following in ~/.vimrc.

    ```set nocompatible```

    ```filetype off```

    ```syntax on```

    ```set rtp+=~/.vim/bundle/Vundle.vim```

    ```call vundle#begin()```

    ```let g:ycm_confirm_extra_conf = 0```

    ```Plugin 'VundleVim/Vundle.vim'```

    ```Plugin 'Valloric/YouCompleteMe'```

    ```autocmd CursorMovedI * if pumvisible() == 0|pclose|endif```

    ```autocmd InsertLeave * if pumvisible() == 0|pclose|endif```

    ```call vundle#end()```

    ```filetype plugin indent on```

* Launch Vim and run the following. Plugin Installation completes with ‘Done!’ at the bottom left. Come out of it using :q.

    ```:PluginInstall```

* Install development tools and CMake.

    ```sudo apt-get install build-essential cmake```

* Install Python Dev.

    ```sudo apt-get install python-dev python3-dev```

* Compiling YCM without semantic support for C-family languages (Installing only for Python).

    ```cd ~/.vim/bundle/YouCompleteMe```

    ```./install.py```

* Test by opening any .py file. When you start typing, we start to see code recommendation and completions.

### **Based on tutorials from:**

[https://github.com/VundleVim/Vundle.vim#quick-start](https://github.com/VundleVim/Vundle.vim#quick-start)

[http://valloric.github.io/YouCompleteMe/#ubuntu-linux-x64](http://valloric.github.io/YouCompleteMe/#ubuntu-linux-x64)

### **These steps might be outdated over time. The best place get the updated tutorial is the follow the above links.**