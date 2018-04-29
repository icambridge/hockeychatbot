from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.components import ComponentBuilder
import sklearn

builder = ComponentBuilder(use_cache=True)
training_data = load_data('training-data.json')
trainer = Trainer(config.load("rasa_config.yml"), builder)
trainer.train(training_data)

model_directory = trainer.persist('./model/')