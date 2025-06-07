# API 测试命令

本文档提供了使用 curl 测试 API 接口的命令示例。

## 用户管理 API

### 创建用户

```bash
# 创建新用户
curl -X POST http://localhost:8000/api/v1/user \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "john_doe",
    "password": "secure_password123",
    "email": "john.doe@example.com",
    "staff_id": "EMP001",
    "role": 1
  }'

# 预期成功响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "user_name": "john_doe",
#     "staff_id": "EMP001",
#     "email": "john.doe@example.com",
#     "status": 0,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }

# 错误响应(邮箱已注册):
# {
#   "code": "409",
#   "message": "Email already registered",
#   "data": null
# }
```

### 获取用户详情

```bash
# 获取用户详情
curl -X GET http://localhost:8000/api/v1/user/d772d20f-fce9-4340-9c6b-b34dabfc3fe6  

# 预期成功响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "d772d20f-fce9-4340-9c6b-b34dabfc3fe6",
#     "user_name": "john_doe",
#     "staff_id": "EMP001",
#     "email": "john.doe@example.com",
#     "status": 0,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }

# 错误响应(未找到):
# {
#   "code": "404",
#   "message": "User not found",
#   "data": null
# }
```

### 获取用户列表

```bash
# 获取用户列表(分页)
curl -X GET "http://localhost:8000/api/v1/user?skip=0&limit=10"

# 预期成功响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "user_id": "550e8400-e29b-41d4-a716-446655440000",
#       "user_name": "john_doe",
#       "staff_id": "EMP001",
#       "email": "john.doe@example.com",
#       "status": 0,
#       "role": 1,
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... 更多用户
#   ]
# }
```

### 更新用户

```bash
# 更新用户信息
curl -X PUT http://localhost:8000/api/v1/user/d772d20f-fce9-4340-9c6b-b34dabfc3fe6 \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "john_smith",
    "email": "john.smith@example.com",
    "status": 1
  }'

# 预期成功响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "user_name": "john_smith",
#     "staff_id": "EMP001",
#     "email": "john.smith@example.com",
#     "status": 1,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### 删除用户

```bash
# 删除用户
curl -X DELETE http://localhost:8000/api/v1/user/550e8400-e29b-41d4-a716-446655440000

# 预期成功响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

## 职位管理 API

### 创建职位

```bash
# 创建新职位
curl -X POST http://localhost:8000/api/v1/job \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "前端开发工程师",
    "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
    "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
    "soft_skills": ["团队协作", "沟通能力", "解决问题能力"]
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "前端开发工程师",
#     "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#     "soft_skills": ["团队协作", "沟通能力", "解决问题能力"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### 获取职位详情

```bash
# 获取职位详情
curl -X GET http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "前端开发工程师",
#     "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#     "soft_skills": ["团队协作", "沟通能力", "解决问题能力"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### 获取职位列表

```bash
# 获取职位列表（分页）
curl -X GET "http://localhost:8000/api/v1/job?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "job_id": "550e8400-e29b-41d4-a716-446655440000",
#       "job_title": "前端开发工程师",
#       "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
#       "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#       "soft_skills": ["团队协作", "沟通能力", "解决问题能力"],
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... 更多职位
#   ]
# }
```

### 更新职位

```bash
# 更新职位信息
curl -X PUT http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "高级前端开发工程师",
    "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Redux", "Next.js"]
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "高级前端开发工程师",
#     "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Redux", "Next.js"],
#     "soft_skills": ["团队协作", "沟通能力", "解决问题能力"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### 删除职位

```bash
# 删除职位
curl -X DELETE http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### 搜索职位

```bash
# 搜索职位
curl -X GET "http://localhost:8000/api/v1/job/search/前端?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "job_id": "550e8400-e29b-41d4-a716-446655440000",
#       "job_title": "前端开发工程师",
#       "job_description": "负责公司产品的前端开发工作，使用React技术栈实现用户界面和交互功能",
#       "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#       "soft_skills": ["团队协作", "沟通能力", "解决问题能力"],
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... 更多匹配的职位
#   ]
# }
```

## 测试管理 API

### 创建测试

```bash
# 创建测试
curl -X POST http://localhost:8000/api/v1/test \
  -H "Content-Type: application/json" \
  -d '{
    "type": "coding",
    "language": "English",
    "difficulty": "medium",
    "job_id": "job001",
    "user_id": "user001",
    "examination_points": ["React", "JavaScript", "前端性能优化"],
    "test_time": 90
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "coding",
#     "language": "English",
#     "difficulty": "medium",
#     "status": "open",
#     "job_id": "job001",
#     "job_title": "前端开发工程师",
#     "user_id": "user001",
#     "user_name": "张三",
#     "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#     "examination_points": ["React", "JavaScript", "前端性能优化"],
#     "test_time": 90,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": null
#   }
# }
```

### 获取测试详情

```bash
# 获取测试详情
curl -X GET http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "coding",
#     "language": "English",
#     "difficulty": "medium",
#     "status": "open",
#     "job_id": "job001",
#     "job_title": "前端开发工程师",
#     "user_id": "user001",
#     "user_name": "张三",
#     "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#     "examination_points": ["React", "JavaScript", "前端性能优化"],
#     "test_time": 90,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": null
#   }
# }
```

### 获取测试列表

```bash
# 获取测试列表（分页）
curl -X GET "http://localhost:8000/api/v1/test?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "前端性能优化"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... 更多测试
#   ]
# }
```

### 更新测试

```bash
# 更新测试
curl -X PUT http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "interview",
    "language": "Chinese",
    "difficulty": "hard",
    "status": "in_progress",
    "job_id": "job002",
    "user_id": "user002",
    "question_ids": ["q001", "q002", "q003", "q004"],
    "examination_points": ["React", "JavaScript", "前端性能优化", "组件设计"],
    "test_time": 120
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "interview",
#     "language": "Chinese",
#     "difficulty": "hard",
#     "status": "in_progress",
#     "job_id": "job002",
#     "job_title": "后端开发工程师",
#     "user_id": "user002",
#     "user_name": "李四",
#     "question_ids": ["q001", "q002", "q003", "q004"],
#     "examination_points": ["React", "JavaScript", "前端性能优化", "组件设计"],
#     "test_time": 120,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": "2024-03-20T11:00:00.000Z"
#   }
# }
```

### 删除测试

```bash
# 删除测试
curl -X DELETE http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### 根据用户ID获取测试

```bash
# 根据用户ID获取测试
curl -X GET "http://localhost:8000/api/v1/test/user/user001?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "前端性能优化"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... 更多该用户的测试
#   ]
# }
```

### 根据职位ID获取测试

```bash
# 根据职位ID获取测试
curl -X GET "http://localhost:8000/api/v1/test/job/job001?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "前端性能优化"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... 更多该职位的测试
#   ]
# }
```

### 根据状态获取测试

```bash
# 根据状态获取测试
curl -X GET "http://localhost:8000/api/v1/test/status/open?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "前端性能优化"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... 更多开放状态的测试
#   ]
# }
```

### 根据类型获取测试

```bash
# 根据类型获取测试
curl -X GET "http://localhost:8000/api/v1/test/type/coding?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "前端性能优化"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... 更多编程类型的测试
#   ]
# }
```

## 错误代码说明

- `400`: 验证错误
- `404`: 资源未找到
- `409`: 资源冲突(如邮箱已注册)
- `422`: 请求格式无效
- `500`: 服务器内部错误 

## 问题管理 API

### 创建问题

```bash
# 创建新问题
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "什么是React的虚拟DOM?",
    "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
    "examination_points": ["React", "虚拟DOM", "性能优化"],
    "job_title": "前端开发工程师",
    "language": "Chinese",
    "difficulty": "medium",
    "type": "short_answer"
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "什么是React的虚拟DOM?",
#     "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#     "examination_points": ["React", "虚拟DOM", "性能优化"],
#     "job_title": "前端开发工程师",
#     "language": "Chinese",
#     "difficulty": "medium",
#     "type": "short_answer"
#   }
# }
```

### 获取问题详情

```bash
# 获取问题详情
curl -X GET http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "什么是React的虚拟DOM?",
#     "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#     "examination_points": ["React", "虚拟DOM", "性能优化"],
#     "job_title": "前端开发工程师",
#     "language": "Chinese",
#     "difficulty": "medium",
#     "type": "short_answer"
#   }
# }
```

### 获取问题列表

```bash
# 获取问题列表（分页）
curl -X GET "http://localhost:8000/api/v1/question?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "什么是React的虚拟DOM?",
#       "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#       "examination_points": ["React", "虚拟DOM", "性能优化"],
#       "job_title": "前端开发工程师",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... 更多问题
#   ]
# }
```

### 更新问题

```bash
# 更新问题
curl -X PUT http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "question": "详细解释React的虚拟DOM及其优势",
    "difficulty": "hard",
    "examination_points": ["React", "虚拟DOM", "性能优化", "渲染机制"]
  }'

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "详细解释React的虚拟DOM及其优势",
#     "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#     "examination_points": ["React", "虚拟DOM", "性能优化", "渲染机制"],
#     "job_title": "前端开发工程师",
#     "language": "Chinese",
#     "difficulty": "hard",
#     "type": "short_answer"
#   }
# }
```

### 删除问题

```bash
# 删除问题
curl -X DELETE http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### 搜索问题

```bash
# 搜索问题
curl -X GET "http://localhost:8000/api/v1/question/search/React?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "什么是React的虚拟DOM?",
#       "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#       "examination_points": ["React", "虚拟DOM", "性能优化"],
#       "job_title": "前端开发工程师",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... 更多匹配的问题
#   ]
# }
```

### 根据岗位获取问题

```bash
# 根据岗位获取问题
curl -X GET "http://localhost:8000/api/v1/question/job/前端开发工程师?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "什么是React的虚拟DOM?",
#       "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#       "examination_points": ["React", "虚拟DOM", "性能优化"],
#       "job_title": "前端开发工程师",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... 更多该岗位的问题
#   ]
# }
```

### 根据难度获取问题

```bash
# 根据难度获取问题
curl -X GET "http://localhost:8000/api/v1/question/difficulty/medium?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "什么是React的虚拟DOM?",
#       "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#       "examination_points": ["React", "虚拟DOM", "性能优化"],
#       "job_title": "前端开发工程师",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... 更多中等难度的问题
#   ]
# }
```

### 根据题目类型获取问题

```bash
# 根据题目类型获取问题
curl -X GET "http://localhost:8000/api/v1/question/type/short_answer?skip=0&limit=10"

# 预期响应:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "什么是React的虚拟DOM?",
#       "answer": "虚拟DOM是React的一个核心概念，它是真实DOM的一个轻量级副本。当组件状态发生变化时，React首先在虚拟DOM中进行更新，然后通过比较(diffing)算法找出真实DOM中需要更新的部分，最后只更新需要更新的部分，从而提高性能。",
#       "examination_points": ["React", "虚拟DOM", "性能优化"],
#       "job_title": "前端开发工程师",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... 更多简答题
#   ]
# }
```

## 聊天 API

### 开始聊天，首次开启面试时候调用

```bash
curl -X POST http://localhost:8000/api/v1/chat/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "user123",
    "test_id": "test456",
    "job_title": "React Web Developer",
    "examination_points": "React, JavaScript, TypeScript, React Router, React State Management, Redux, React Hooks, React Context API, React Performance Optimization",
    "test_time": 3,
    "language": "English",
    "difficulty": "easy"
  }'
```

### 提交用户回答的问题，同时返回面试官的新消息

```bash
curl -X POST http://localhost:8000/api/v1/chat/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "user123",
    "test_id": "test456",
    "question_id": "question789",
    "user_answer": "React的虚拟DOM是一种内存中的数据结构，它代表了UI的理想状态。当应用状态改变时，React首先在虚拟DOM中进行更新，然后通过Diffing算法比较新旧虚拟DOM的差异，最后只将差异部分应用到实际DOM中，从而提高性能。"
  }' 