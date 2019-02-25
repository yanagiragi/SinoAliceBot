import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# Get an example image
import matplotlib.cbook as cbook
image_file = cbook.get_sample_data('C:\\Users\\Ragi\\Desktop\\test.png')
img = plt.imread(image_file)

pointstr = """192 287
196 284
199 281
202 278
205 276
208 274
210 272
212 270
214 268
216 266
218 264
220 262
222 261
224 260
225 259
239 247
240 259
241 270
242 281
243 291
244 300
245 309
246 317
247 324
248 331
249 337
250 343
251 349
252 354
252 359
251 426
251 431
251 436
251 441
251 445
251 449
251 453
251 456
251 459
251 462
251 465
251 468
251 470
251 472
251 474
232 497
227 497
223 497
219 497
215 497
212 497
209 497
206 497
203 497
200 497
198 497
196 497
194 497
192 497
190 497
153 487
149 486
145 485
141 484
138 483
135 482
132 481
129 480
127 480
125 480
123 480
121 480
119 480
117 480
115 480
84 460
83 455
82 450
81 445
80 441
80 437
80 433
80 430
80 427
80 424
80 421
80 418
80 416
80 414
80 412
69 370
72 366
75 362
78 359
81 356
83 353
85 350
87 347
89 345
91 343
93 341
95 339
96 337
97 335
98 333"""

points = pointstr.split('\n')

pointsX = []
pointsY = []

for i in range(0, len(points)):
    pointsXX, pointsYY = points[i].split(' ')
    pointsX.append(float(pointsXX))
    pointsY.append(float(pointsYY))

# Make some example data
x = pointsX
y = pointsY

print(x, y)

# Create a figure. Equal aspect so circles look circular
fig,ax = plt.subplots(1)
ax.set_aspect('equal')

# Show the image
ax.imshow(img)

# Now, loop through coord arrays, and create a circle at each x,y pair
for xx,yy in zip(x,y):
    circ = Circle((xx,yy),5)
    ax.add_patch(circ)

# Show the image
plt.show()