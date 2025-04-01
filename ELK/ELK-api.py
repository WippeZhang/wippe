from elasticsearch import Elasticsearch

# 连接到 Elasticsearch 实例
es = Elasticsearch("http://10.0.90.131:9200")

# 查询 TOP-N 流量数据，flow exporter 为 10.200.2.197 且目的地为特定国家
response = es.search(index="elastiflow-*", body={
    "query": {
        "bool": {
            "must": [
                {
                    "match_phrase": {
                        "host.name": "10.200.2.197"  # flow exporter IP 匹配
                    }
                }
            ],
            "should": [
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Finland"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Germany"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Sweden"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Russia"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "United Kingdom"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Netherlands"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Norway"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Faroe Islands"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Italy"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "Malta"
                    }
                },
                {
                    "match_phrase": {
                        "destination.geo.country_name": "France"
                    }
                }
            ],
            "minimum_should_match": 1  # 至少匹配一个国家
        }
    }
})

# 打印查询结果
print(response)