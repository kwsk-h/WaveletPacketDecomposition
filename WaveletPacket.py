"""Wavelet Packet Decomposition."""
# -*- coding: utf-8 -*-
import numpy as np

class WaveletPacket:  # ウェーブレットパケット展開

    def __init__(self, max_level):
        self.max_level = max_level  # max_levelまで展開 (2^level個に分割する)
        self.level_num = [2**x for x in range(self.max_level)]  # 各レベル 指定した回数だけ繰り返す
        self.W = np.zeros((self.max_level+1, self.level_num[self.max_level-1]*2)).tolist()  # list 中に各levelでのWavelet係数を入れる

        self.__p = np.array([0.482962913145, 0.836516303738, 0.224143868042, -0.129409522551])  # ドベシイの数列 N=2 ,スケーリング関数(低域成分)
        self.__q = np.array([self.__p[len(self.__p)-n-1]*(-1)**n for n in range(len(self.__p))])  # ウェーブレット関数(高域成分)

        # 抽出
        self.extract_num = 2**self.max_level
        self.output_signal = []  # 出力用


    def WPD(self, X):
        """ Wavelet Packet Decomposition.
            ----------------------------------
            X : input signal (1D numpy array or 1D list)
            ----------------------------------
                                  ┌[H]-W(2.3)┴…
                    ┌[H]-W(1.1)┴[L]-W(2.2)┬…
              W(0.0)┤
                    └[L]-W(1.0)┬[H]-W(2.1)┴…
                                  └[L]-W(2.0)┬…

                level0|  level1  |  level2  |
            ----------------------------------"""
        self.W[0][0] = np.array(X)  # 1ch分のデータ -> W[0][0] にNumpy配列として格納
        le = len(X)  # 信号長
        if self.W[0][0].ndim != 1:
            print("[ERROR] input must be a 1D numpy array or 1D list.")
            print("now :", self.W[0][0].ndim)
            return

        for j in range(1, self.max_level+1):
            for i in range(self.level_num[j-1]):  # 各レベル 指定した回数だけ繰り返す(2^(j-1)回が基本)
                __s0 = self.W[j-1][i]
                # 高速 Wavelet 変換 (1回で2個に分かれる)
                self.W[j][2*i] = np.array([np.inner(self.__p, np.array([__s0[(n+2*times)%le] for n in range(len(self.__p))]))
                                           for times in range(int((le-2)/2))])
                self.W[j][2*i+1] = np.array([np.inner(self.__q, np.array([__s0[(n+2*times)%le] for n in range(len(self.__q))]))
                                             for times in range(int((le-2)/2))])
            le = int((le-2)/2)  # ダウンサンプリング


    def output(self, level, extract_num):
        """ Wからoutput_signalへ.
            ----------------------------
            self.Wの(level)層からextract_num個抽出して，self.output_signalへ
            W(level, 0)はスキップ

            input level : [int]参照する展開レベル
            return self.output_signal
            ---------------------------- """
        if level > self.max_level or level < 0:  # levelがおかしい場合self.max_levelにする
            level = self.max_level
        if extract_num < self.extract_num:
            self.extract_num = extract_num
        self.output_signal = [self.W[level][k+1] for k in range(self.extract_num)]
        return self.output_signal
