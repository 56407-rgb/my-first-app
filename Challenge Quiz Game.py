import tkinter as tk
from tkinter import messagebox

class SmartShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panda Cafe - Smart Shop & Discount")
        self.root.geometry("420x550")
        self.root.resizable(False, False)
        
        # 1. ชื่อร้านค้า
        tk.Label(root, text="🐼 Panda Cafe ☕", font=("Tahoma", 18, "bold"), fg="#3e2723").pack(pady=10)
        
        # 2. สินค้า 4 รายการ (ชื่อรายการ, ราคาต่อชิ้น)
        self.items = [
            ("เอสเปรสโซ่ (Espresso)", 50),
            ("ชาเขียว (Green Tea)", 55),
            ("เค้กสตรอว์เบอร์รี่ (Cake)", 85),
            ("คุกกี้ช็อกโกแลต (Cookie)", 40)
        ]
        
        frame_items = tk.LabelFrame(root, text=" เลือกจำนวนสินค้า ", font=("Tahoma", 10, "bold"))
        frame_items.pack(fill="x", padx=20, pady=5)
        
        self.qty_entries = []
        for name, price in self.items:
            row = tk.Frame(frame_items)
            row.pack(fill="x", padx=10, pady=4)
            
            tk.Label(row, text=f"{name} ({price} บาท)", font=("Tahoma", 10), width=26, anchor="w").pack(side="left")
            entry = tk.Entry(row, width=6, justify="center", font=("Tahoma", 10))
            entry.insert(0, "0")
            entry.pack(side="right")
            self.qty_entries.append((price, entry))
            
        # เงื่อนไขสมาชิก
        self.is_member = tk.BooleanVar()
        tk.Checkbutton(root, text="มีบัตรสมาชิก (ลดเพิ่ม 50 บาท)", variable=self.is_member, font=("Tahoma", 10)).pack(pady=5)
        
        # ปุ่มคำนวณราคารวม
        tk.Button(root, text="คำนวณราคารวมและส่วนลด", bg="#4CAF50", fg="white", font=("Tahoma", 10, "bold"), 
                  command=self.calculate_total, relief="groove").pack(pady=8)
        
        # ส่วนแสดงผลราคา
        self.lbl_total = tk.Label(root, text="ราคารวม: 0.00 บาท", font=("Tahoma", 10))
        self.lbl_total.pack()
        
        self.lbl_discount = tk.Label(root, text="ส่วนลด: 0.00 บาท", font=("Tahoma", 10))
        self.lbl_discount.pack()
        
        self.lbl_net = tk.Label(root, text="ยอดที่ต้องจ่ายจริง: 0.00 บาท", font=("Tahoma", 11, "bold"), fg="#d32f2f")
        self.lbl_net.pack(pady=5)
        
        # ส่วนรับเงินสดและเงินทอน
        frame_pay = tk.Frame(root)
        frame_pay.pack(pady=10)
        
        tk.Label(frame_pay, text="รับเงินจากลูกค้า (บาท):", font=("Tahoma", 10)).pack(side="left", padx=5)
        self.entry_cash = tk.Entry(frame_pay, width=10, font=("Tahoma", 10), justify="center")
        self.entry_cash.pack(side="left")
        
        tk.Button(root, text="ชำระเงิน / คำนวณเงินทอน", bg="#1976D2", fg="white", font=("Tahoma", 10, "bold"), 
                  command=self.process_payment).pack(pady=5)
        
        self.lbl_change = tk.Label(root, text="เงินทอน: - บาท", font=("Tahoma", 12, "bold"), fg="#2e7d32")
        self.lbl_change.pack(pady=5)
        
        self.net_price = 0.0

    def calculate_total(self):
        try:
            total_price = 0.0
            for price, entry in self.qty_entries:
                qty = int(entry.get())
                if qty < 0:
                    raise ValueError
                total_price += price * qty
                
            discount = 0.0
            
            # --- 3. เกณฑ์ส่วนลด (If-Else) ---
            # เงื่อนไขที่ 1: ซื้อครบ 300 บาท ลด 10%
            if total_price >= 300:
                discount += total_price * 0.10
                
            # เงื่อนไขที่ 2: มีบัตรสมาชิก ลดเพิ่ม 50 บาท
            if self.is_member.get():
                discount += 50.0
                
            # ป้องกันส่วนลดเกินราคารวม
            if discount > total_price:
                discount = total_price
                
            self.net_price = total_price - discount
            
            # แสดงผล
            self.lbl_total.config(text=f"ราคารวม: {total_price:,.2f} บาท")
            self.lbl_discount.config(text=f"ส่วนลด: {discount:,.2f} บาท")
            self.lbl_net.config(text=f"ยอดที่ต้องจ่ายจริง: {self.net_price:,.2f} บาท")
            
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนสินค้าเป็นตัวเลขจำนวนเต็มบวก")

    def process_payment(self):
        try:
            cash = float(self.entry_cash.get())
            if cash < self.net_price:
                messagebox.showwarning("เตือน", "เงินที่ได้รับไม่เพียงพอกับยอดชำระ!")
            else:
                change = cash - self.net_price
                self.lbl_change.config(text=f"เงินทอน: {change:,.2f} บาท")
                messagebox.showinfo("สำเร็จ", f"ชำระเงินเรียบร้อย!\nยอดชำระ: {self.net_price:,.2f} บาท\nรับเงินมา: {cash:,.2f} บาท\nเงินทอน: {change:,.2f} บาท")
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินเป็นตัวเลขที่ถูกต้อง")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartShopApp(root)
    root.mainloop()
