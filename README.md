# Spring Ninja Game Automated

### Game Description
This is a Sigle Player Game.

Playstore Link: [Spring Ninja](https://play.google.com/store/apps/details?id=com.ketchapp.springninja&hl=en)

![Image](/Images/spring1.png)
![Image](/Images/spring2.png)

#### Difficulty level
Medium

#### Overview

Compress (press the screen) the spring so that Ninja can jump to next Pole.  

#### Requirements
- Computer with OpenCV-Python, Scikit-Learn, ADB Tool and required drivers set up.
- An Android Device with the Spring Ninja game installed on it. (Turn on the Developer options for better visualization)
- USB data transfer cable.

#### Block Diagram

![BlockDiagram](/Images/BlockDiagram.png)

#### Tutorial
##### Step 1: Using ADB Tool to capture screenshot
The following command instantaneously takes the screenshot of the connected device and stores it in the SD card following the specified path.

```python
  from subprocess import call
  call(['adb', 'shell', 'screencap', '/sdcard/spring.png'])
```

The following command pulls it from the SD card of the android device into the working system following the path specified

```python
	from subprocess import call
	call(['adb', 'pull', '/sdcard/spring.png'])
```

The pulled image is stored in the form of a matrix of pixel values by the Opencv.
```python
	im = cv2.imread('spring.png')
```


#### Step 2: Image processing

Once the screenshot is obtained, Position of Player and Pole and Target Pole centre is calculated using color masking and Contours Finding Method.

#### Step 3: Algorithm

I have created sample [dataset](/data.csv) manually, we are going to train our **neural network** using this
dataset.
```python
	# train_X: contains horizontal and vertical distance between two poles
	# train_y: time in milliseconds to goto from one pole to other
	from sklearn.neural_network import MLPRegressor
    regr = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50, max_iter=1000, random_state=1)
	regr.fit(train_X, train_y)
```

#### Step 4: Using ADB Tool to simulate touch

The following command presses at the point on the screen with the co-ordinates mentioned as (360, 640). This is used to simulate for touch_time
```python
	# x: horizontal distance
	# y: vertical distance
	time = int(regr.predict([[x,y]]))
    cmd = ['adb', 'shell', 'input', 'swipe', '360', '640', '360', '640']
    cmd.append(str(time))
    call(cmd)
```
### Testing

After connecting your phone to laptop with satisfied envrionment.
check phone is connected or not, with command

```bash
	adb devices
```
if device is connected and not authorized it will show in output otherwise it will show device-id and device.

##### Now start game and click play and run the solver script

```bash
	python spring.py
```

The Game was tested on 1280x720 android device (Moto G3), for other device score may change
