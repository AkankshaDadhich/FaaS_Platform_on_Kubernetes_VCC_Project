id=$1

kubectl delete deployment random-quotes-$id
kubectl delete service random-quotes$id-service