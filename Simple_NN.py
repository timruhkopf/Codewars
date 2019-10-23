import tensorflow as tf

x = tf.constant([1,2,3,4,5])
y = tf.constant([1,2,2,1,1])

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x, y, epochs=5)
model.evaluate(x, y)


