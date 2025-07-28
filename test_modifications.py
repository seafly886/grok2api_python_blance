#!/usr/bin/env python3
"""
测试修改后的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import AuthTokenManager

def test_key_mode_functionality():
    """测试key模式功能"""
    print("=== 测试Key模式功能 ===")
    
    # 创建token管理器实例
    token_manager = AuthTokenManager()
    
    # 测试设置key模式
    print("1. 测试设置轮询模式...")
    result = token_manager.set_key_mode('polling', 20)
    assert result == True, "设置轮询模式失败"
    
    mode_info = token_manager.get_key_mode_info()
    assert mode_info['mode'] == 'polling', "轮询模式设置不正确"
    assert mode_info['usage_limit'] == 20, "使用次数限制设置不正确"
    print("✓ 轮询模式设置成功")
    
    print("2. 测试设置单key循环模式...")
    result = token_manager.set_key_mode('single', 15)
    assert result == True, "设置单key循环模式失败"
    
    mode_info = token_manager.get_key_mode_info()
    assert mode_info['mode'] == 'single', "单key循环模式设置不正确"
    assert mode_info['usage_limit'] == 15, "使用次数限制设置不正确"
    print("✓ 单key循环模式设置成功")
    
    print("3. 测试无效模式...")
    result = token_manager.set_key_mode('invalid', 20)
    assert result == False, "应该拒绝无效模式"
    print("✓ 无效模式正确被拒绝")
    
    print("=== Key模式功能测试通过 ===\n")

def test_model_config():
    """测试模型配置"""
    print("=== 测试模型配置 ===")
    
    token_manager = AuthTokenManager()
    
    # 检查是否包含所有必要的模型
    expected_models = [
        'grok-3', 'grok-3-deepsearch', 'grok-3-deepersearch', 
        'grok-3-reasoning', 'grok-4', 'grok-4-reasoning'
    ]
    
    print("1. 检查normal配置...")
    for model in expected_models:
        assert model in token_manager.model_normal_config, f"模型 {model} 不在normal配置中"
    print("✓ normal配置包含所有必要模型")
    
    print("2. 检查super配置...")
    for model in expected_models:
        assert model in token_manager.model_super_config, f"模型 {model} 不在super配置中"
    print("✓ super配置包含所有必要模型")
    
    print("=== 模型配置测试通过 ===\n")

def test_token_operations():
    """测试token操作"""
    print("=== 测试Token操作 ===")
    
    token_manager = AuthTokenManager()
    
    # 添加测试token
    test_token = {
        "token": "sso-rw=test123;sso=test123",
        "type": "normal"
    }
    
    print("1. 测试添加token...")
    token_manager.add_token(test_token, True)
    
    # 检查token是否被正确添加
    all_tokens = token_manager.get_all_tokens()
    assert test_token["token"] in all_tokens, "Token未被正确添加"
    print("✓ Token添加成功")
    
    print("2. 测试获取token状态...")
    status_map = token_manager.get_token_status_map()
    assert "test123" in status_map, "Token状态未被正确记录"
    print("✓ Token状态获取成功")
    
    print("3. 测试删除token...")
    result = token_manager.delete_token(test_token["token"])
    assert result == True, "Token删除失败"
    
    all_tokens_after = token_manager.get_all_tokens()
    assert test_token["token"] not in all_tokens_after, "Token未被正确删除"
    print("✓ Token删除成功")
    
    print("=== Token操作测试通过 ===\n")

if __name__ == "__main__":
    print("开始测试修改后的功能...\n")
    
    try:
        test_key_mode_functionality()
        test_model_config()
        test_token_operations()
        
        print("🎉 所有测试通过！修改功能正常工作。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)
