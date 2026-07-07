# Glossary

## Agent
An opencode role with a specific responsibility, such as backend, frontend, worker, QA, or review.

## Issue-driven development
A development process where every change starts with a GitHub Issue and ends with a PR linked to that issue.

## VideoJob
A persisted record representing one submitted YouTube processing task.

## Worker
A standalone process that consumes RabbitMQ messages and performs one pipeline step.

## Contract
A shared schema for API payloads, queue messages, statuses, and response shapes.

## Pipeline
The ordered asynchronous process from URL submission to completed digest.

## Adapter
A wrapper around external tools or services such as yt-dlp, ffmpeg, or Groq.

## Handler
A testable function containing worker business logic.

## Fake dependency
A test replacement for external dependencies. Used to keep tests deterministic.
