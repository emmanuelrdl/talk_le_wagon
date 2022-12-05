from datetime import date


def test_auto_doc(date: date, age: int) -> int:
    """_summary_

    Args:
        date (date): _description_
        age (int): _description_

    Returns:
        int: _description_
    """
  print(date)
  print(age)
  return age