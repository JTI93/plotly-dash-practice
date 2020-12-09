# Task 1
import numpy as np
import pandas as pd

# Task 2
np.random.seed(101)

# Task 3
t3 = np.random.randint(1, 101, (100, 5))

# Task 4
t4 = pd.DataFrame(data=t3)

# Task 5
t4.columns = ['f1', 'f2', 'f3', 'f4', 'label']

# Task 6
t6 = pd.DataFrame(data=np.random.randint(0, 101, (50,4)), columns=['A', 'B', 'C', 'D'])

print(t6)