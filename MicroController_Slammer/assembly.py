@micropython.asm_thumb
def flash_led(r0, r1, r2, r3):
	movwt(r5, stm.TIM6)
	movwt(r4, 1)
	str(r4, [r5, stm.TIM_CR1])
	movwt(r4, 0x20)
	str(r4, [r5, stm.TIM_CR2])
	movwt(r5, stm.DAC)
	movwt(r4, 0x70007)
	str(r4, [r5, stm.DAC_CR])
	movw(r6, 2)
	udiv(r4, r1, r6)
	str(r4, [r5, stm.DAC_DHR12R2])
	b(loop_entry)
	label(loop1)
	movw(r4, 0x0)
	str(r4, [r5, stm.DAC_DHR12R1])
	movwt(r4, stm.TIM6)
	label(delay_on)
	ldr(r4, [r4, stm.TIM_SR])
	cmp(r4, 1)
	blt(delay_on)
	mov(r4, r1)
	str(r4, [r5, stm.DAC_DHR12R1])
	movwt(r4, stm.TIM6)
	label(delay_off)
	ldr(r4, [r4, stm.TIM_SR])
	cmp(r4, 1)
	blt(delay_off)
	sub(r0, r0, 1)
	label(loop_entry)
	cmp(r0, 0)
	bgt(loop1)