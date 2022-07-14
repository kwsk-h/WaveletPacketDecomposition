# WaveletPacketDecomposition
## Wavelet Packet Decomposition

(ウェーブレットパケット展開)

----------------------------------
```
                   ┌[H]-W(2.3)┴…
                   |
        ┌[H]-W(1.1)┴[L]-W(2.2)┬…
  W(0.0)┤
        └[L]-W(1.0)┬[H]-W(2.1)┴…
                   |
                   └[L]-W(2.0)┬…

level 0 |  level 1 |  level 2 |
```
----------------------------------


```python
from WaveletPacketDecomposition import WaveletPacket as WP
level = xxx
ex_num = yyy
wpd = WP.WaveletPacket(level)
wpd.WPD(data)
wpd.output(level=level, extract_num=ex_num)
```
