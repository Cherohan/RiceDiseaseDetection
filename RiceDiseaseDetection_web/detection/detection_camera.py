import cv2
import numpy as np

class Onnx_clf:
    def __init__(self, onnx:str='./best_simple.onnx', img_size=640, classlist:list=['BacterialBlight',
                                                                            'BacterialStripe',
                                                                            'Borer',
                                                                            'BrownSpot',
                                                                            'Healthy',
                                                                            'Hispa',
                                                                            'LeafBlast',
                                                                            'LeafRoller',
                                                                            'LeafSmut',
                                                                            'LeafTipBlight',
                                                                            'Moth',
                                                                            'Planthopper',
                                                                            'Stalk',
                                                                            'Trichoborer',
                                                                            'Tungro']) -> None:
        '''	@func: 读取onnx模型,并进行目标识别
            @para	onnx:模型路径
                 	img_size:输出图片大小,和模型直接相关
                    classlist:类别列表
            @return: None
        '''
        self.net = cv2.dnn.readNet(onnx) # 读取模型
        self.img_size = img_size # 输出图片尺寸大小
        self.classlist = classlist # 读取类别列表

    def img_identify(self, img, ifshow=True) -> np.ndarray:
        '''	@func: 图片识别
            @para	img: 图片路径或者图片数组
                    ifshow: 是否显示图片
            @return: 图片数组
        '''
        if type(img) == str: src = cv2.imread(img)
        else: src = img
        height, width, _ = src.shape #注意输出的尺寸是先高后宽
        _max = max(width, height)
        resized = np.zeros((_max, _max, 3), np.uint8)
        resized[0:height, 0:width] = src  # 将图片转换成正方形，防止后续图片预处理(缩放)失真
        # 图像预处理函数,缩放裁剪,交换通道  img     scale              out_size              swapRB
        blob = cv2.dnn.blobFromImage(resized, 1/255.0, (self.img_size, self.img_size), swapRB=True)
        prop = _max / self.img_size  # 计算缩放比例
        dst = cv2.resize(src, (round(width/prop), round(height/prop)))
        print(prop)  # 注意，这里不能取整，而是需要取小数，否则后面绘制框的时候会出现偏差
        self.net.setInput(blob) # 将图片输入到模型
        out = self.net.forward() # 模型输出
        print(out.shape)
        out = np.array(out[0])
        out = out[out[:, 4] >= 0.5]  # 利用numpy的花式索引,速度更快, 过滤置信度低的目标   !!!调整置信度
        boxes = out[:, :4]
        confidences = out[:, 4]
        class_ids = np.argmax(out[:, 5:], axis=1)
        class_scores = np.max(out[:, 5:], axis=1)
        # out2 = out[0][out[0][:][4] > 0.5]
        # for i in out[0]: # 遍历每一个框
        #     class_max_score = max(i[5:])
        #     if i[4] < 0.5 or class_max_score < 0.25: # 过滤置信度低的目标
        #         continue
        #     boxes.append(i[:4]) # 获取目标框: x,y,w,h (x,y为中心点坐标)
        #     confidences.append(i[4]) # 获取置信度
        #     class_ids.append(np.argmax(i[5:])) # 获取类别id
        #     class_scores.append(class_max_score) # 获取类别置信度
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45) # 非极大值抑制, 获取的是索引
        # print(indexes)
        iffall = True if len(indexes)!=0 else False
        # print(iffall)
        for i in indexes:   # 遍历每一个目标, 绘制目标框
            box = boxes[i]
            class_id = class_ids[i]
            score = round(class_scores[i], 2)
            x1 = round((box[0] - 0.5*box[2])*prop)
            y1 = round((box[1] - 0.5*box[3])*prop)
            x2 = round((box[0] + 0.5*box[2])*prop)
            y2 = round((box[1] + 0.5*box[3])*prop)
            # print(x1, y1, x2, y2)
            self.drawtext(src,(x1, y1), (x2, y2), self.classlist[class_id]+' '+str(score))
            dst = cv2.resize(src, (round(width/prop), round(height/prop)))
        if ifshow:
            cv2.imshow('result', dst)
            cv2.waitKey(0)
        return dst, iffall

    def video_identify(self, cap:str) -> None:
        cap = cv2.VideoCapture(0)
        fps = 120
        cap.set(5, fps)  # 帧率
        #fps = cap.get(cv2.CAP_PROP_FPS)
        #print(fps)
        while cap.isOpened():
            ret, frame = cap.read()
            #键盘输入空格暂停，输入q退出
            key = cv2.waitKey(1) & 0xff
            if key == ord(" "): cv2.waitKey(1000//60)
            if key == ord("q"): break
            if not ret: break
            img, res = self.img_identify(frame, False)
            cv2.imshow('result', img)
            print(res)
            key = cv2.waitKey(1000//60)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break

    @staticmethod
    def drawtext(image, pt1, pt2, text):
        '''	@func: 根据给出的坐标和文本,在图片上进行绘制
            @para	image: 图片数组; pt1: 左上角坐标; pt2: 右下角坐标; text: 矩形框上显示的文本,即类别信息
            @return: None
        '''
        fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL  # 字体
        # fontFace = cv2.FONT_HERSHEY_COMPLEX  # 字体
        fontScale = 1.5  # 字体大小
        line_thickness = 3  # 线条粗细
        font_thickness = 2  # 文字笔画粗细
        line_back_color = (0, 0, 255)  # 线条和文字背景颜色:红色
        font_color = (255, 255, 255)  # 文字颜色:白色

        # 绘制矩形框
        cv2.rectangle(image, pt1, pt2, color=line_back_color, thickness=line_thickness)
        # 计算文本的宽高: retval:文本的宽高; baseLine:基线与最低点之间的距离(本例未使用)
        retval, baseLine = cv2.getTextSize(text,fontFace=fontFace,fontScale=fontScale, thickness=font_thickness)
        # 计算覆盖文本的矩形框坐标
        topleft = (pt1[0], pt1[1] - retval[1]) # 基线与目标框上边缘重合(不考虑基线以下的部分)
        bottomright = (topleft[0] + retval[0], topleft[1] + retval[1])
        cv2.rectangle(image, topleft, bottomright, thickness=-1, color=line_back_color) # 绘制矩形框(填充)
        # 绘制文本
        cv2.putText(image, text, pt1, fontScale=fontScale,fontFace=fontFace, color=font_color, thickness=font_thickness)

if __name__ == '__main__':
    clf = Onnx_clf()
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    tk.Tk().withdraw() # 隐藏主窗口, 必须要用，否则会有一个小窗口
    # source = askopenfilename(title="打开保存的图片或视频")
    print('摄像头开启中...按q退出')
    clf.video_identify(0)