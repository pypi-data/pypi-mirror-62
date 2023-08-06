# Achilles

Model file Manager

### 模型管理

#### 创建项目
![创建项目](docs/images/achilles_project.jpg)

#### 创建模型
![创建模型](docs/images/achilles_model.jpg)

#### 创建模型文件
![创建模型文件](docs/images/achilles_model_version.png)

### 模型使用

```python
# 引入model
from achilles.model import *
# 使用项目、模型、版本实例化model
model = Model("nlp_server", "emotional_classification", "0.0.1")
# 将模型下载到指定文件 
model.download_model("./model.model") 

```