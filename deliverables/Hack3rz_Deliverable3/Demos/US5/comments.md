In US5 we wanted to address the scaling of our microservices in order to introduce redundancies that prevent request from being rejected when a service is not available anymore.
We introduced a load balancer and scaled both the annotation and the prediction services to two instances per service. Nginx is running
on a separate docker container and forwards the requests to the respective instances using a round-robin protocol.

Caveats:
- There is no automatic service discovery yet (hostnames of services are manually configured in the nginx config)
- There is no healthcheck on the services other than docker restarting the services if a crash occurred