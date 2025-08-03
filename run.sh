current_port=$(cat current_port.txt)
port=$((current_port-1))
sed -i "s/random-quotes.*/random-quotes-$current_port/g" register.yml
sed -i "s/$port/$current_port/g" register.yml 


next_port=$((current_port+1))
echo $next_port > current_port.txt

kubectl apply -f register.yml
kubectl expose deployment random-quotes-$current_port --port=$current_port --name=random-quotes$current_port-service
sleep 90
kubectl port-forward service/random-quotes$current_port-service $current_port:$current_port &

# current_port=$((current_port+1))
# echo $current_port > current_port.txt
