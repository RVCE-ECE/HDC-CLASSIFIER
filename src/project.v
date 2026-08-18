`default_nettype none

module tt_um_hdc_classifier (
    input  wire [7:0] ui_in,    // 8-bit data stream chunk
    output wire [7:0] uo_out,   // Result outputs
    input  wire [7:0] uio_in,   // Control signals
    output wire [7:0] uio_out,  
    output wire [7:0] uio_oe,   
    input  wire       ena,      
    input  wire       clk,      
    input  wire       rst_n     
);

    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    wire mode        = uio_in[0];
    wire class_sel   = uio_in[1];
    wire valid_in    = uio_in[2];
    wire start_query = uio_in[3];

    reg [63:0] class_a_reg;
    reg [63:0] class_b_reg;

    reg [6:0] dist_a;
    reg [6:0] dist_b;
    reg [2:0] chunk_cnt;
    reg       done_flag;

    wire [7:0] xor_a = ui_in ^ class_a_reg[63:56];
    wire [7:0] xor_b = ui_in ^ class_b_reg[63:56];

    wire [3:0] pop_a = xor_a[0] + xor_a[1] + xor_a[2] + xor_a[3] + 
                       xor_a[4] + xor_a[5] + xor_a[6] + xor_a[7];

    wire [3:0] pop_b = xor_b[0] + xor_b[1] + xor_b[2] + xor_b[3] + 
                       xor_b[4] + xor_b[5] + xor_b[6] + xor_b[7];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            class_a_reg <= 64'b0;
            class_b_reg <= 64'b0;
            dist_a      <= 7'b0;
            dist_b      <= 7'b0;
            chunk_cnt   <= 3'b0;
            done_flag   <= 1'b0;
        end else if (ena) begin
            if (start_query) begin
                dist_a    <= 7'b0;
                dist_b    <= 7'b0;
                chunk_cnt <= 3'b0;
                done_flag <= 1'b0;
            end 
            else if (valid_in) begin
                if (mode == 1'b0) begin
                    if (class_sel == 1'b0)
                        class_a_reg <= {class_a_reg[55:0], ui_in};
                    else
                        class_b_reg <= {class_b_reg[55:0], ui_in};
                end 
                else begin
                    class_a_reg <= {class_a_reg[55:0], class_a_reg[63:56]};
                    class_b_reg <= {class_b_reg[55:0], class_b_reg[63:56]};

                    dist_a <= dist_a + pop_a;
                    dist_b <= dist_b + pop_b;

                    chunk_cnt <= chunk_cnt + 1'b1;
                    if (chunk_cnt == 3'd7) begin
                        done_flag <= 1'b1;
                    end
                end
            end
        end
    end

    wire       winner      = (dist_b < dist_a);
    wire [6:0] winning_val = winner ? dist_b : dist_a;

    assign uo_out[7]   = done_flag;
    assign uo_out[6]   = winner;
    assign uo_out[5:0] = winning_val[5:0];

endmodule
