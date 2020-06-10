set -euxo pipefail

echo -e "\033[32m $(git version) \033[0m"

git config user.name ""
git config user.email ""

cd ~/blog/Avalon

git pull origin master
#whereis rvm
/path/to/.rvm/gems/ruby-2.7.0/wrappers/bundle install
/path/to/.rvm/gems/ruby-2.7.0/wrappers/jekyll build

exit 0
