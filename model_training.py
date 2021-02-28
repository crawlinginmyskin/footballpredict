import pandas as pd
import tensorflow as tf

model_input = pd.read_csv('model_input.csv', index_col=[0])
model_targets = model_input.iloc[:, 22]
model_input = model_input.drop(columns=['22'])


model = tf.keras.Sequential([tf.keras.layers.Dense(22),
                            tf.keras.layers.Dense(242, activation=tf.nn.softmax),
                            tf.keras.layers.Dense(121, activation=tf.nn.softmax),
                            tf.keras.layers.Dense(3, activation=tf.nn.softmax)])
model.compile(optimizer='RMSprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(model_input.values, model_targets.values, validation_split=0.2, shuffle=True, batch_size=20, epochs=250)
