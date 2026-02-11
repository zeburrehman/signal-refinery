/**
 * Utility library functions
 * Place reusable utility functions here
 */

export const cn = (...classes: (string | undefined | false)[]) => {
  return classes.filter(Boolean).join(" ");
};
