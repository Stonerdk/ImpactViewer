### ImpactViewer
- 오른쪽 발의 CoP를 계산하여, 이전 CoP와의 거리가 가장 큰 지점을 Impact로 측정했습니다.
- ratio가 가장 큰 지점부터 측정했습니다.

### 테스트 결과
```
./data\driver01.txt  : evaluated impact time =  60 real impact time =  59 error =  -1
./data\driver02.txt  : evaluated impact time =  66 real impact time =  67 error =  1
./data\driver03.txt  : evaluated impact time =  86 real impact time =  86 error =  0
./data\driver05.txt  : evaluated impact time =  82 real impact time =  81 error =  -1
./data\driver06.txt  : evaluated impact time =  49 real impact time =  50 error =  1
./data\driver07.txt  : evaluated impact time =  53 real impact time =  51 error =  -2
./data\driver08.txt  : evaluated impact time =  62 real impact time =  61 error =  -1
./data\driver09.txt  : evaluated impact time =  61 real impact time =  61 error =  0
./data\driver10.txt  : evaluated impact time =  64 real impact time =  65 error =  1
./data\driver11.txt  : evaluated impact time =  56 real impact time =  57 error =  1
./data\driver12.txt  : evaluated impact time =  63 real impact time =  61 error =  -2
./data\driver13.txt  : evaluated impact time =  56 real impact time =  58 error =  2
./data\driver14.txt  : evaluated impact time =  56 real impact time =  56 error =  0
```


### 개선사항
- tkinter을 사용해서 상호작용을 구현하려 했으나, 그래프 확대 축소가 어려워 pyplot의 widget을 대신 사용했습니다.
- pyplot의 다양한 기능을 그대로 쓸 수 있는 UI를 사용하면 좋을 것 같습니다.