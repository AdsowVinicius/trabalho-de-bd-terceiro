// Design System - TERCEIRIZE+ Theme
export const colors = {
  primary: '#0B7A47',
  primaryDark: '#055A35',
  primaryLight: '#1B9456',
  primaryVeryLight: '#E8F5ED',
  white: '#FFFFFF',
  lightGray: '#F5F5F5',
  gray: '#E0E0E0',
  darkGray: '#9E9E9E',
  text: '#2C3E50',
  textLight: '#5F6C7B',
  danger: '#E74C3C',
  dangerDark: '#C0392B',
  warning: '#F39C12',
  success: '#0B7A47',
  info: '#3498DB'
};

export const shadows = {
  sm: '0 2px 8px rgba(11, 122, 71, 0.08)',
  md: '0 4px 12px rgba(11, 122, 71, 0.12)',
  lg: '0 8px 24px rgba(11, 122, 71, 0.15)',
  xl: '0 16px 40px rgba(11, 122, 71, 0.2)'
};

export const transitions = {
  default: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  fast: 'all 0.15s ease-out',
  slow: 'all 0.5s ease-in-out'
};

export const borderRadius = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  full: '50%'
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '20px',
  xxl: '24px',
  xxxl: '30px'
};

export const typography = {
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif',
  h1: {
    fontSize: '36px',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.5px'
  },
  h2: {
    fontSize: '28px',
    fontWeight: 700,
    lineHeight: 1.3,
    letterSpacing: '-0.3px'
  },
  h3: {
    fontSize: '20px',
    fontWeight: 600,
    lineHeight: 1.4
  },
  body: {
    fontSize: '14px',
    fontWeight: 400,
    lineHeight: 1.6
  },
  bodySmall: {
    fontSize: '12px',
    fontWeight: 400,
    lineHeight: 1.5
  }
};

export const breakpoints = {
  mobile: '480px',
  tablet: '768px',
  desktop: '1024px',
  wide: '1200px'
};

export const gradients = {
  primary: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primaryLight} 100%)`,
  primaryDark: `linear-gradient(135deg, ${colors.primaryDark} 0%, ${colors.primary} 100%)`,
  primaryToWhite: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.white} 100%)`
};

// Utility function to generate consistent button styles
export const buttonStyles = (variant = 'primary') => {
  const variants = {
    primary: {
      background: colors.primary,
      color: colors.white,
      border: 'none',
      boxShadow: shadows.sm,
      '&:hover': {
        background: colors.primaryDark,
        boxShadow: shadows.md,
        transform: 'translateY(-2px)'
      }
    },
    secondary: {
      background: colors.lightGray,
      color: colors.text,
      border: `2px solid ${colors.gray}`,
      boxShadow: shadows.sm,
      '&:hover': {
        background: colors.gray,
        boxShadow: shadows.md
      }
    },
    danger: {
      background: colors.danger,
      color: colors.white,
      border: 'none',
      boxShadow: shadows.sm,
      '&:hover': {
        background: colors.dangerDark,
        boxShadow: shadows.md,
        transform: 'translateY(-2px)'
      }
    },
    outline: {
      background: 'transparent',
      color: colors.primary,
      border: `2px solid ${colors.primary}`,
      boxShadow: 'none',
      '&:hover': {
        background: colors.primaryVeryLight,
        boxShadow: shadows.sm
      }
    }
  };

  return variants[variant] || variants.primary;
};

// Export as default theme object
export default {
  colors,
  shadows,
  transitions,
  borderRadius,
  spacing,
  typography,
  breakpoints,
  gradients,
  buttonStyles
};
