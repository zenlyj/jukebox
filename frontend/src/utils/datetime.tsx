export const getMonthName = (month: number): string => {
  if (month < 1 || month > 12) {
    return "";
  }
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return months[month - 1];
};

export const padNum = (num: number): string => {
  return num < 10 ? `0${num}` : `${num}`;
};
