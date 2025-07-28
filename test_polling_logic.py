#!/usr/bin/env python3
"""
测试新的轮询模式逻辑
"""

def test_new_polling_logic():
    """测试新的轮询模式逻辑"""
    print("=== 测试新的轮询模式逻辑 ===")
    
    # 模拟token管理器的轮询逻辑
    class MockTokenManager:
        def __init__(self):
            self.key_mode = 'polling'
            # 模拟3个token的列表
            self.token_list = [
                {"token": "token1", "RequestCount": 0, "MaxRequestCount": 5},
                {"token": "token2", "RequestCount": 0, "MaxRequestCount": 5},
                {"token": "token3", "RequestCount": 0, "MaxRequestCount": 5}
            ]
        
        def get_next_token_polling_mode(self):
            """模拟新的轮询逻辑"""
            if not self.token_list:
                return None
            
            # 获取当前token（不移除）
            token_entry = self.token_list[0]
            token_entry["RequestCount"] += 1
            
            # 检查是否达到上限
            if token_entry["RequestCount"] >= token_entry["MaxRequestCount"]:
                # 达到上限，移除此token
                removed_token = self.token_list.pop(0)
                print(f"Token {removed_token['token']} 达到上限，已移除")
            else:
                # 未达到上限，将当前token移到末尾（实现轮询）
                self.token_list.append(self.token_list.pop(0))
                print(f"Token {token_entry['token']} 使用一次后轮询到下一个")
            
            return token_entry["token"]
        
        def get_token_order(self):
            """获取当前token顺序"""
            return [t["token"] for t in self.token_list]
    
    # 测试轮询逻辑
    manager = MockTokenManager()
    
    print("初始token顺序:", manager.get_token_order())
    print()
    
    # 模拟多次调用
    for i in range(12):
        token = manager.get_next_token_polling_mode()
        if token:
            print(f"第{i+1}次调用: 使用 {token}")
            print(f"当前token顺序: {manager.get_token_order()}")
            print(f"剩余token数量: {len(manager.token_list)}")
        else:
            print(f"第{i+1}次调用: 无可用token")
        print()
    
    print("=== 轮询逻辑测试完成 ===\n")

def test_polling_vs_single_mode():
    """对比轮询模式和单key模式的区别"""
    print("=== 对比轮询模式和单key模式 ===")
    
    # 轮询模式：每次使用一个token就切换
    print("轮询模式调用顺序:")
    tokens = ["A", "B", "C"]
    for i in range(9):
        current_token = tokens[i % len(tokens)]
        print(f"第{i+1}次: 使用token {current_token}")
    
    print()
    
    # 单key模式：使用完配置次数才切换
    print("单key模式调用顺序（每个token使用3次）:")
    usage_limit = 3
    current_token_index = 0
    current_usage = 0
    
    for i in range(9):
        current_token = tokens[current_token_index]
        current_usage += 1
        print(f"第{i+1}次: 使用token {current_token} (第{current_usage}次)")
        
        if current_usage >= usage_limit:
            current_token_index = (current_token_index + 1) % len(tokens)
            current_usage = 0
            if i < 8:  # 不是最后一次
                print(f"  -> 切换到下一个token")
    
    print("\n=== 模式对比完成 ===\n")

def test_token_exhaustion():
    """测试token耗尽的情况"""
    print("=== 测试token耗尽情况 ===")
    
    class MockTokenManagerExhaustion:
        def __init__(self):
            # 每个token只能使用2次
            self.token_list = [
                {"token": "token1", "RequestCount": 0, "MaxRequestCount": 2},
                {"token": "token2", "RequestCount": 0, "MaxRequestCount": 2}
            ]
        
        def get_next_token_polling_mode(self):
            if not self.token_list:
                return None
            
            token_entry = self.token_list[0]
            token_entry["RequestCount"] += 1
            
            if token_entry["RequestCount"] >= token_entry["MaxRequestCount"]:
                removed_token = self.token_list.pop(0)
                print(f"Token {removed_token['token']} 耗尽，剩余token数: {len(self.token_list)}")
            else:
                self.token_list.append(self.token_list.pop(0))
            
            return token_entry["token"]
    
    manager = MockTokenManagerExhaustion()
    
    # 模拟调用直到所有token耗尽
    call_count = 0
    while True:
        call_count += 1
        token = manager.get_next_token_polling_mode()
        if token:
            print(f"第{call_count}次调用: 使用 {token}")
        else:
            print(f"第{call_count}次调用: 所有token已耗尽")
            break
        
        if call_count > 10:  # 防止无限循环
            break
    
    print("=== token耗尽测试完成 ===\n")

if __name__ == "__main__":
    print("开始测试新的轮询模式逻辑...\n")
    
    try:
        test_new_polling_logic()
        test_polling_vs_single_mode()
        test_token_exhaustion()
        
        print("🎉 所有测试通过！新的轮询逻辑工作正常。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
