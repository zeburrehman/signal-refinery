/**
 * Utility functions
 * Place specific utility functions here
 */

export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat("en-US").format(date);
};
