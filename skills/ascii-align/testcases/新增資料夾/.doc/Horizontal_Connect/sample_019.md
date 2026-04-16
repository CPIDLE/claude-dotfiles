## Sample 019

**Source**: `AMRCoolDown_v0\case01\mqtt分析.md` L175

```
斷線期間：
  ├─ Client 端：buffer 10 條 --> 5 秒溢出 --> 後續全部 error [-12] 丟棄
  ├─ Broker 端：clean_session=true --> 不保留離線訊息
  └─ 協議層：QoS=0 --> 不重試

重連後：
  ├─ buffer 清空 --> 之前的都丟了
  ├─ broker 無保留 --> 不補發
  └─ 新訊息才開始收到 --> 但 GyrobotLayer 5 秒後才算恢復
```

