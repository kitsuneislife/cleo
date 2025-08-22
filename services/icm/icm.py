"""ICM stub implementation"""
import math

def intrinsic_reward(error, clip_max=10.0):
    v = math.log1p(error)
    v = max(0.0, min(v, clip_max))
    # normalize to 0..1
    return v / clip_max

if __name__ == "__main__":
    print(intrinsic_reward(0.1))
