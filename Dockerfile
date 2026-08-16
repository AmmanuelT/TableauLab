# Stage 1: Install dependencies

FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install locked dependencies for the build
RUN npm ci

# Stage 2: Build the application
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from the deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source files
COPY . .

# Disable Next.js telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

# Build the Next.js application
RUN npm run build

# Stage 3: Production runtime
FROM node:20-alpine AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create a non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy the standalone output
COPY --from=builder /app/.next/standalone ./

# Copy static files - these are not included in standalone
COPY --from=builder /app/.next/static ./.next/static

# Copy public directory for static assets
COPY --from=builder /app/public ./public

# Set ownership to the non-root user
RUN chown -R nextjs:nodejs /app

USER nextjs

# Cloud Run uses the PORT environment variable
EXPOSE 8080
ENV PORT=8080
ENV HOSTNAME="0.0.0.0"

# The standalone output includes a minimal server.js
CMD ["node", "server.js"]