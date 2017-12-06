import boto3

class Common:

    def __init__(self):
        self.cw = boto3.client(
            'cloudwatch',
            region_name='ap-northeast-1'
        )

    def cw_put_metric(self, namespace, metric_name, metric_value, dimensions_name, dimensions_value):
        self.cw.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Unit': 'Count',
                    'Value': metric_value,
                    'Dimensions':[
                        {
                            'Name':dimensions_name,
                            'Value':dimensions_value
                        }
                    ]
                },
            ]
        )
