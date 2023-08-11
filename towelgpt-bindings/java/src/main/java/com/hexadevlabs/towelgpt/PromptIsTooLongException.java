package com.hexadevlabs.towelgpt;

public class PromptIsTooLongException extends RuntimeException {
    public PromptIsTooLongException(String message) {
        super(message);
    }
}
