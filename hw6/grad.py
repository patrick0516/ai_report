import numpy as np

class Tensor:
    def __init__(self, data, _children=(), _op=''):
        """
        初始化一個Tensor物件。

        參數:
        data -- 數值數據，支持numpy陣列或標量。
        _children -- 生成此Tensor的父節點集合，用於構建計算圖。
        _op -- 生成此Tensor的操作符名稱（用於調試和可視化）。
        """
        self.data = np.array(data)  # 將數據轉換為numpy陣列
        self.grad = np.zeros(self.data.shape)  # 初始化梯度為零
        self._backward = lambda: None  # 預設的反向傳播函數
        self._prev = set(_children)  # 生成此節點的前置節點
        self._op = _op  # 生成此節點的操作符

    @property
    def shape(self):
        return self.data.shape
    
    def __add__(self, other):
        """
        實現Tensor的加法操作。

        參數:
        other -- 另一個Tensor物件或數值。

        返回:
        out -- 加法結果的Tensor物件。
        """
        other = other if isinstance(other, Tensor) else Tensor(np.zeros(self.shape) + other)  # 讓維度一致
        out = Tensor(self.data + other.data, (self, other), '+')  # 生成新的Tensor物件

        def _backward():
            self.grad += out.grad  # 將輸出的梯度傳遞給self
            other.grad += out.grad  # 將輸出的梯度傳遞給other
        out._backward = _backward

        return out

    def __mul__(self, other):
        """
        實現Tensor的乘法操作。

        參數:
        other -- 另一個Tensor物件或數值。

        返回:
        out -- 乘法結果的Tensor物件。
        """
        other = other if isinstance(other, Tensor) else Tensor(np.zeros(self.shape) + other)  # 讓維度一致
        out = Tensor(self.data * other.data, (self, other), '*')  # 生成新的Tensor物件

        def _backward():
            self.grad += other.data * out.grad  # 將輸出的梯度傳遞給self
            other.grad += self.data * out.grad  # 將輸出的梯度傳遞給other
        out._backward = _backward

        return out

    def __pow__(self, other):
        """
        實現Tensor的冪運算。

        參數:
        other -- 冪指數，只支持int或float類型。

        返回:
        out -- 冪運算結果的Tensor物件。
        """
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Tensor(self.data ** other, (self,), f'**{other}')  # 生成新的Tensor物件

        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad  # 反向傳播公式
        out._backward = _backward

        return out

    def relu(self):
        """
        實現ReLU激活函數。

        返回:
        out -- ReLU激活結果的Tensor物件。
        """
        out = Tensor(np.maximum(0, self.data), (self,), 'relu')  # 生成新的Tensor物件

        def _backward():
            self.grad += (out.data > 0) * out.grad  # 反向傳播公式
        out._backward = _backward

        return out

    def matmul(self, other):
        """
        實現矩陣乘法。

        參數:
        other -- 另一個Tensor物件。

        返回:
        out -- 矩陣乘法結果的Tensor物件。
        """
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(np.matmul(self.data, other.data), (self, other), 'matmul')  # 生成新的Tensor物件

        def _backward():
            self.grad += np.dot(out.grad, other.data.T)  # 反向傳播公式
            other.grad += np.dot(self.data.T, out.grad)  # 反向傳播公式
        out._backward = _backward

        return out

    def softmax(self):
        """
        實現Softmax函數。

        返回:
        out -- Softmax結果的Tensor物件。
        """
        out = Tensor(np.exp(self.data) / np.sum(np.exp(self.data), axis=1)[:, None], (self,), 'softmax')
        softmax = out.data

        def _backward():
            s = np.sum(out.grad * softmax, 1)
            t = np.reshape(s, [-1, 1])  # 重新塑形為 n*1
            self.grad += (out.grad - t) * softmax
        out._backward = _backward

        return out

    def log(self):
        """
        實現自然對數函數。

        返回:
        out -- 自然對數結果的Tensor物件。
        """
        out = Tensor(np.log(self.data), (self,), 'log')

        def _backward():
            self.grad += out.grad / self.data  # 反向傳播公式
        out._backward = _backward

        return out

    def sum(self, axis=None):
        """
        實現求和操作。

        參數:
        axis -- 求和的軸。

        返回:
        out -- 求和結果的Tensor物件。
        """
        out = Tensor(np.sum(self.data, axis=axis), (self,), 'SUM')

        def _backward():
            output_shape = np.array(self.data.shape)
            output_shape[axis] = 1
            tile_scaling = self.data.shape // output_shape
            grad = np.reshape(out.grad, output_shape)
            self.grad += np.tile(grad, tile_scaling)
        out._backward = _backward

        return out

    def cross_entropy(self, yb):
        """
        實現交叉熵損失函數。

        參數:
        yb -- 標籤的Tensor物件。

        返回:
        loss -- 交叉熵損失的Tensor物件。
        """
        log_probs = self.log()
        zb = yb * log_probs
        outb = zb.sum(axis=1)
        loss = -outb.sum()  # 交叉熵損失
        return loss  # 不需要指定反向傳播，調用 loss.backward() 就能反向傳播

    def backward(self):
        """
        實現反向傳播。

        通過拓撲排序所有的節點，然後應用鏈式法則計算梯度。
        """
        # 拓撲排序計算圖中的所有節點
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        build_topo(self)

        # 從輸出節點開始，逆序應用鏈式法則計算梯度
        self.grad = np.ones_like(self.data)  # 將輸出節點的梯度初始化為1
        for v in reversed(topo):
            v._backward()

    def __neg__(self):  # -self
        return self * -1

    def __radd__(self, other):  # other + self
        return self + other

    def __sub__(self, other):  # self - other
        return self + (-other)

    def __rsub__(self, other):  # other - self
        return other + (-self)

    def __rmul__(self, other):  # other * self
        return self * other

    def __truediv__(self, other):  # self / other
        return self * other**-1

    def __rtruediv__(self, other):  # other / self
        return other * self**-1

    def __repr__(self):
        return f"Tensor(data={self.data}, grad={self.grad})"
