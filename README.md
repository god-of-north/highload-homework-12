# Homework #12 for Highload:Projector

**Redis vs Beanstalkd**

Set up 3 containers - beanstalkd and redis (rdb and aof)

Write 2 simple scripts: 1st should put message into queue, 2nd should read from queue.

Configure storing to disk, and compare queues performance.


## Instllation

```
git clone https://github.com/god-of-north/highload-homework-12.git
cd highload-homework-12
docker-compose build
```

## Using

To put message in queue:
```
curl -X GET "localhost:5000/publish_beanstalkd?size=1024&batch=5"
curl -X GET "localhost:5000/publish_redis_rdb?size=1024&batch=5"
curl -X GET "localhost:5000/publish_redis_aof?size=1024&batch=5"
```

To run Siege tests:
```
docker-compose run --rm siege -c25 -t10s -b "http://producer:5000/publish_beanstalkd?size=64&batch=1"
docker-compose run --rm siege -c25 -t10s -b "http://producer:5000/publish_redis_rdb?size=64&batch=1"
docker-compose run --rm siege -c25 -t10s -b "http://producer:5000/publish_redis_aof?size=64&batch=1"
```

## Test results

Beanstalkd:
```
Concurrency                        1                10                50                 1                10                50
Message size:                     64 bytes          64 bytes          64 bytes        1024 bytes        1024 bytes        1024 bytes
Transactions:                   4724 hits         6060 hits         5716 hits         2787 hits         2518 hits         2891 hits
Availability:                 100.00 %          100.00 %          100.00 %          100.00 %          100.00 %          100.00 %
Elapsed time:                   9.07 secs         9.86 secs         9.54 secs         9.73 secs         9.20 secs         9.78 secs
Data transferred:               0.01 MB           0.01 MB           0.01 MB           0.01 MB           0.00 MB           0.01 MB
Response time:                  0.00 secs         0.02 secs         0.08 secs         0.00 secs         0.04 secs         0.17 secs
Transaction rate:             520.84 trans/sec  614.60 trans/sec  599.16 trans/sec  286.43 trans/sec  273.70 trans/sec  295.60 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                    0.97              9.95             49.76              0.98              9.96             49.53
Successful transactions:        4724              6060              5716              2787              2518              2891
Failed transactions:               0                 0                 0                 0                 0                 0
Longest transaction:            0.01              0.07              0.12              0.01              0.09              0.25
Shortest transaction:           0.00              0.01              0.01              0.00              0.00              0.01
```

Redis RDB:
```
Concurrency                        1                10                50                 1                10                50                1               10               50
Message size:                     64 bytes          64 bytes          64 bytes        1024 bytes        1024 bytes        1024 bytes    1048576 bytes    1048576 bytes    1048576 bytes
Transactions:                   4781 hits         6015 hits         5993 hits         2643 hits         2750 hits         2831 hits           6 hits           5 hits           5 hits
Availability:                 100.00 %          100.00 %          100.00 %          100.00 %          100.00 %          100.00 %         100.00 %         100.00 %         100.00 %
Elapsed time:                   9.35 secs         9.48 secs         9.38 secs         9.35 secs         9.10 secs         9.34 secs        9.81 secs        9.12 secs        9.43 secs
Data transferred:               0.01 MB           0.01 MB           0.01 MB           0.01 MB           0.01 MB           0.01 MB          0.00 MB          0.00 MB          0.00 MB
Response time:                  0.00 secs         0.02 secs         0.08 secs         0.00 secs         0.03 secs         0.16 secs        1.45 secs        4.82 secs        4.86 secs
Transaction rate:             511.34 trans/sec  634.49 trans/sec  638.91 trans/sec  282.67 trans/sec  302.20 trans/sec  303.10 trans/sec   0.61 trans/sec   0.55 trans/sec   0.53 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec      0.00 MB/sec      0.00 MB/sec      0.00 MB/sec
Concurrency:                    0.97              9.95             49.57              0.98              9.96             49.57             0.89             2.64             2.57
Successful transactions:        4781              6015              5993              2643              2750              2831                6                5                5
Failed transactions:               0                 0                 0                 0                 0                 0                0                0                0
Longest transaction:            0.01              0.03              0.12              0.08              0.06              0.24             1.57             8.05             8.03
Shortest transaction:           0.00              0.01              0.01              0.00              0.01              0.01             1.40             0.00             0.00
```

Redis AOF:
```
Concurrency                        1                10                50                 1                10                50                    1           10               50
Message size:                     64 bytes          64 bytes          64 bytes        1024 bytes        1024 bytes        1024 bytes    1048576 bytes    1048576 bytes    1048576 bytes
Transactions:                   3291 hits         3972 hits         3684 hits         1987 hits         2334 hits         2142 hits           5 hits           6 hits           5 hits
Availability:                 100.00 %          100.00 %          100.00 %          100.00 %          100.00 %          100.00 %         100.00 %         100.00 %         100.00 %
Elapsed time:                   9.21 secs         9.28 secs         9.90 secs         9.19 secs         9.72 secs         9.62 secs        9.87 secs        9.98 secs        9.13 secs
Data transferred:               0.01 MB           0.01 MB           0.01 MB           0.00 MB           0.00 MB           0.00 MB          0.00 MB          0.00 MB          0.00 MB
Response time:                  0.00 secs         0.02 secs         0.13 secs         0.00 secs         0.04 secs         0.22 secs        1.83 secs        5.76 secs        5.09 secs
Transaction rate:             357.33 trans/sec  428.02 trans/sec  372.12 trans/sec  216.21 trans/sec  240.12 trans/sec  222.66 trans/sec   0.51 trans/sec   0.60 trans/sec   0.55 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec       0.00 MB/sec      0.00 MB/sec      0.00 MB/sec      0.00 MB/sec
Concurrency:                    0.97              9.95             49.55              0.99              9.97             49.42             0.93             3.46             2.79
Successful transactions:        3291              3972              3684              1987              2334              2142                5                6                5
Failed transactions:               0                 0                 0                 0                 0                 0                0                0                0
Longest transaction:            0.01              0.05              0.29              0.01              0.06              0.32             2.13             9.87             8.47
Shortest transaction:           0.00              0.00              0.01              0.00              0.01              0.02             1.61             0.00             0.00
```
