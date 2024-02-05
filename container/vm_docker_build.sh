set -e
base_image=$1
branch=$2
subbranch=$3
repo=$4

current_branch=$(git branch --show-current)
#if [ "$current_branch" != "$subbranch" ]; then
#  echo "Not on $subbranch branch" >&2
#  exit 1
#fi

git add .
git commit -m 'docker build' || true
git push
sleep 1

#git checkout $branch
#git merge $subbranch
#sleep 1

# https://linuxhint.com/install-docker-debian/
echo $base_image
git add .
git commit -m 'docker build' || true
git push
branch=$(git branch --show-current)
echo branch $branch
sleep 1

command="cd ~/$repo &&
git fetch &&
git checkout $branch &&
git pull &&
docker build -f container/Dockerfile --tag $base_image . &&
docker push $base_image"
echo $command


gcloud compute ssh "docker-demo" --zone=europe-west1-b --command="${command}"

sleep 1

# gcloud compute ssh "docker" --zone=europe-west1-b --command="echo ola"

#gcloud compute ssh "docker" --zone=europe-west1-b --command="docker system prune -a --volumes --force"

git checkout $current_branch
