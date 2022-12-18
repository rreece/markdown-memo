#!/usr/bin/env bash
#
# install.sh
#
# Installs dependencies for markdown-memo.
#
# See: https://github.com/rreece/markdown-memo
#
# author:  Ryan Reece  <http://rreece.github.io/>
# created: 2022-12-18
#
###############################################################################


get_os()
{
    local _GET_OS="unknown"
    local _UNAME_OS=$(uname)
    case "${_UNAME_OS}" in
        Darwin)
            _GET_OS="mac"
        ;;
        Linux)
            _GET_OS="linux"
        ;;
        *)  
            true
        ;;
    esac
    echo ${_GET_OS}
}

install_for_mac()
{
    echo "Installing for mac..."

}

install_for_linux()
{
    echo "Installing for linux..."
    sudo apt-get -y update
    sudo apt-get -y install make
    sudo apt-get -y install texlive-latex-extra
    sudo apt-get -y install pandoc
#    pandoc-citeproc
#    pandoc-crossref
#    https://askubuntu.com/questions/1335772/using-pandoc-crossref-on-ubuntu-20-04

    wget -c https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.10.0a/pandoc-crossref-Linux.tar.xz
    tar -xf pandoc-crossref-Linux.tar.xz
    sudo mv pandoc-crossref /usr/local/bin/
    sudo chmod a+x /usr/local/bin/pandoc-crossref
    sudo mkdir -p /usr/local/man/man1
    sudo mv pandoc-crossref.1  /usr/local/man/man1

#    matplotlib
#    xpdf
}


GET_OS=$(get_os)

case "${GET_OS}" in
    mac)
        install_for_mac
    ;;
    linux)
        install_for_linux
    ;;
    *)  
        true
    ;;
esac

