## Sample 249

**Source**: `personal-rag_v2\PKB\vault\docs\TM-Program-Analysis\docs\UNIFIED_UI_TM_TEACH_PLAN.md` L206

```
tmflow_domain_client/
├─ proto/
│  └─ TmDomainService.proto          # 從 TM release 拷貝
├─ _generated/                        # grpc_tools.protoc 產出
│  ├─ TmDomainService_pb2.py
│  └─ TmDomainService_pb2_grpc.py
├─ client.py                          # Channel / stub 管理
├─ session.py                         # TeachSession context manager
├─ teach.py                           # 高階 helpers (jog_cartesian, save_point, ...)
├─ models.py                          # dataclass 對應 proto message
└─ tests/
   ├─ test_with_mock_server.py        # 用 grpcio testing 起 mock server
   └─ test_integration.py             # 需連真機，gated by env var
```

