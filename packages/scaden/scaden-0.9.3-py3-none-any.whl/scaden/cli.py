"""
cdn Command Line Interface
author: Kevin Menden, DZNE Tübingen

This is the main file for executing the cdn program.
"""

# imports
import click
import scaden
from scaden.scaden_main import training, prediction, processing

@click.group()
@click.version_option('1.0.0')
def cli():
    pass


"""
Training mode
"""
@cli.command()
@click.argument(
    'data_path',
    type = click.Path(exists=True),
    required = True,
    metavar = '<training data>'
)
@click.option(
    '--train_datasets',
    default = '',
    help = 'Datasets used for training. Uses all by default.'
)
@click.option(
    '--model_dir',
    default = "./",
    help = 'Path to store the model in'
)
@click.option(
    '--batch_size',
    default = 128,
    help = 'Batch size to use for training. Default: 128'
)
@click.option(
    '--learning_rate',
    default = 0.0001,
    help = 'Learning rate used for training. Default: 0.0001'
)
@click.option(
    '--steps',
    default = 20000,
    help = 'Number of training steps'
)
def train(data_path, train_datasets, model_dir, batch_size, learning_rate, steps):
    """ Train a cdn model """
    training(data_path=data_path,
                      train_datasets=train_datasets,
                      model_dir=model_dir,
                      batch_size=batch_size,
                      learning_rate=learning_rate,
                      num_steps=steps)


"""
Prediction mode
"""
@cli.command()
@click.argument(
    'data_path',
    type = click.Path(exists=True),
    required = True,
    metavar = '<prediction data>'
)
@click.option(
    '--model_dir',
    default = "./",
    help = 'Path to trained model'
)
@click.option(
    '--outname',
    default = "scaden_predictions.txt",
    help = 'Name of predictions file.'
)
def predict(data_path, model_dir, outname):
    """ cdn prediction using a trained model """
    prediction(model_dir=model_dir,
                        data_path=data_path,
                        out_name=outname)



"""
Processing mode
"""
@cli.command()
@click.argument(
    'data_path',
    type = click.Path(exists=True),
    required = True,
    metavar = '<training dataset to be processed>'
)
@click.argument(
    'prediction_data',
    type = click.Path(exists=True),
    required = True,
    metavar = '<data for prediction>'
)
@click.option(
    '--processed_path',
    default = "processed.h5ad",
    help = 'Path of processed file. Must end with .h5ad'
)
@click.option(
    '--var_cutoff',
    default = 0.1,
    help = 'Filter out genes with a variance less than the specified cutoff. A low cutoff is recommended,'
           'this should only remove genes that are obviously uninformative.'
)
def process(data_path, prediction_data, processed_path, var_cutoff):
    """ Process a dataset for training """
    processing(data_path=prediction_data,
                        training_data=data_path,
                        processed_path=processed_path,
                        var_cutoff=var_cutoff
               )

def main():
    text = """
     ____                _            
    / ___|  ___ __ _  __| | ___ _ __  
    \___ \ / __/ _` |/ _` |/ _ \ '_ \ 
     ___) | (_| (_| | (_| |  __/ | | |
    |____/ \___\__,_|\__,_|\___|_| |_|

    """
    click.echo(click.style(text, fg='blue'))
    cli()

