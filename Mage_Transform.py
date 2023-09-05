import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    df = df.drop_duplicates().reset_index(drop = True)
    df['Trip_id'] = df.index
    
    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop = True)
    datetime_dim['tpep_pickup_datetime'] = datetime_dim['tpep_pickup_datetime']
    datetime_dim['pickup_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pickup_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pickup_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pickup_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pickup_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

    datetime_dim['tpep_dropoff_datetime'] = datetime_dim['tpep_dropoff_datetime']
    datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday

    datetime_dim['datetime_id'] = datetime_dim.index
    datetime_dim = datetime_dim[['datetime_id','tpep_pickup_datetime','pickup_hour','pickup_day','pickup_month',
                             'pickup_year','pickup_weekday','tpep_dropoff_datetime','drop_hour','drop_day',
                            'drop_month','drop_year','drop_weekday']]
    

    passenger_dim = df[['passenger_count']].reset_index(drop = True)
    passenger_dim['passenger_id'] = passenger_dim.index
    passenger_dim = passenger_dim[['passenger_id','passenger_count']]
    
    tripdistance_dim = df[['trip_distance']].reset_index(drop = True)
    tripdistance_dim['tripdistance_id'] = tripdistance_dim.index
    tripdistance_dim['trip_distance'] = tripdistance_dim['trip_distance']
    tripdistance_dim = tripdistance_dim[['tripdistance_id','trip_distance']]

    ratecode_type ={
        1:"Standard rate",
        2:"JFK",
        3:"Newark",
        4:"Nassau or Westchester",
        5:"Negotiated fare",
        6:"Group ride"
    }
    ratecode_dim = df[['RatecodeID']].reset_index(drop = True )
    ratecode_dim['ratecodeID'] = ratecode_dim['RatecodeID']
    ratecode_dim['rc_id'] = ratecode_dim.index
    ratecode_dim['ratecode_name'] = ratecode_dim['RatecodeID'].map(ratecode_type)
    ratecode_dim = ratecode_dim[['rc_id','ratecodeID','ratecode_name']]

    
    
    pickup_loc_dim = df[['pickup_longitude','pickup_latitude']].reset_index(drop = True)
    pickup_loc_dim['pickup_loc_id'] = pickup_loc_dim.index
    #pickup_loc_dim['pickup_longitude'] = pickup_loc_dim['pickup_longitude']
    #pickup_loc_dim['pickup_latitude'] = pickup_loc_dim['pickup_latitude']
    pickup_loc_dim = pickup_loc_dim[['pickup_loc_id','pickup_longitude','pickup_latitude']]

    drop_loc_dim = df[['dropoff_longitude','dropoff_latitude']].reset_index(drop = True)
    drop_loc_dim['drop_loc_id'] = drop_loc_dim.index
    drop_loc_dim = drop_loc_dim[['drop_loc_id','dropoff_longitude','dropoff_latitude']]

    payment_type_name = {
        1:"Credit card",
        2:"Cash",
        3:"No charge",
        4:"Dispute",
        5:"Unknown",
        6:"Voided trip"
    }

    payment_type_dim = df[['payment_type']].reset_index(drop = True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type_id'].map(payment_type_name)
    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']]

    fact_table = df.merge(datetime_dim, left_on = 'Trip_id', right_on = 'datetime_id') 
                   .merge(passenger_dim,left_on = 'Trip_id', right_on = 'passenger_id')
                   .merge(tripdistance_dim,left_on = 'Trip_id', right_on = 'tripdistance_id')  
                   .merge(ratecode_dim,left_on = 'Trip_id', right_on = 'rc_id')  
                   .merge(pickup_loc_dim,left_on = 'Trip_id', right_on = 'pickup_loc_id') 
                   .merge(drop_loc_dim,left_on = 'Trip_id', right_on = 'drop_loc_id') 
                   .merge(payment_type_dim,left_on = 'Trip_id', right_on = 'payment_type_id') 
                    [['Trip_id','VendorID', 'datetime_id', 'passenger_id',
                      'tripdistance_id', 'rc_id', 'store_and_fwd_flag', 'pickup_loc_id', 'drop_loc_id',
                      'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
                      'improvement_surcharge', 'total_amount']]    



    return {"datetime_dim":datetime_dim.to_dict(orient="dict"),
    "passenger_dim":passenger_dim.to_dict(orient="dict"),
    "tripdistance_dim":tripdistance_dim.to_dict(orient="dict"),
    "ratecode_dim":ratecode_dim.to_dict(orient="dict"),
    "pickup_loc_dim":pickup_loc_dim.to_dict(orient="dict"),
    "drop_loc_dim":drop_loc_dim.to_dict(orient="dict"),
    "payment_type_dim":payment_type_dim.to_dict(orient="dict"),
    "fact_table":fact_table.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

