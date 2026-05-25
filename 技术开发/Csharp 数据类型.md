 C# 是一种强类型语言，这意味着在声明变量时必须指定其数据类型。数据类型决定了变量可以存储的数据种类、占用的内存大小以及可以对它执行的操作。

C# 的数据类型主要分为两大类：**值类型 (Value Types)** 和 **引用类型 (Reference Types)**。此外，还有一些特殊的类型如指针类型（不常用，主要用于非安全代码）。

---

### 一、值类型 (Value Types)

值类型变量直接包含它们的值。当您将一个值类型变量赋给另一个变量时，会复制该值。它们通常存储在栈 (Stack) 上。

**主要特点：**
*   直接存储数据。
*   赋值时是值的拷贝。
*   通常存储在栈上（或作为引用类型对象的字段存储在堆上）。
*   派生自 `System.ValueType`。

**常见值类型：**

1.  **整数类型 (Integral Types):** 用于存储整数。
    *   `sbyte`: 8 位有符号整数 (-128 到 127)
    *   `byte`: 8 位无符号整数 (0 到 255)
    *   `short`: 16 位有符号整数 (-32,768 到 32,767)
    *   `ushort`: 16 位无符号整数 (0 到 65,535)
    *   `int`: 32 位有符号整数 (-2,147,483,648 到 2,147,483,647) - **最常用**
    *   `uint`: 32 位无符号整数 (0 到 4,294,967,295)
    *   `long`: 64 位有符号整数 (-9,223,372,036,854,775,808 到 9,223,372,036,854,775,807)
    *   `ulong`: 64 位无符号整数 (0 到 18,446,744,073,709,551,615)

    **使用场景：** 计数、索引、年龄、数量等。
    ```csharp
    int age = 30;
    long population = 7_000_000_000L; // long 类型字面量需要 L 后缀
    byte level = 255;
    ```

2.  **浮点类型 (Floating-Point Types):** 用于存储带小数的数字。
    *   `float`: 32 位单精度浮点数 (精度较低，约 6-9 位小数)
    *   `double`: 64 位双精度浮点数 (精度较高，约 15-17 位小数) - **最常用**
    *   `decimal`: 128 位高精度十进制数 (精度极高，约 28-29 位小数，避免浮点运算误差)

    **使用场景：**
    *   `float`: 科学计算、图形处理（对精度要求不高，但性能敏感的场景）。
    *   `double`: 大多数科学计算、几何计算。
    *   `decimal`: **货币计算、金融数据**（必须使用，避免精度问题）。

    ```csharp
    float piFloat = 3.1415926535f; // float 类型字面量需要 f 后缀
    double piDouble = 3.141592653589793; // double 是默认浮点类型，不需要后缀
    decimal salary = 50000.75m; // decimal 类型字面量需要 m 后缀
    ```

3.  **布尔类型 (Boolean Type):**
    *   `bool`: 只能存储 `true` 或 `false`。

    **使用场景：** 条件判断、开关状态。
    ```csharp
    bool isActive = true;
    bool hasPermission = false;
    ```

4.  **字符类型 (Character Type):**
    *   `char`: 16 位 Unicode 字符，用于存储单个字符。

    **使用场景：** 存储单个字母、数字、符号。
    ```csharp
    char initial = 'J';
    char symbol = '$';
    ```

5.  **枚举类型 (Enum Types):**
    *   `enum`: 用户自定义的值类型，用于定义一组命名的常量。

    **使用场景：** 表示有限的、离散的状态或选项。
    ```csharp
    public enum DayOfWeek
    {
        Sunday,
        Monday,
        Tuesday,
        Wednesday,
        Thursday,
        Friday,
        Saturday
    }

    DayOfWeek today = DayOfWeek.Wednesday;
    ```

6.  **结构体类型 (Struct Types):**
    *   `struct`: 用户自定义的值类型，可以包含字段、方法、属性等。与类 (class) 类似，但结构体是值类型。

    **使用场景：** 当类型表示一个轻量级的数据结构，且其行为更像值而不是对象时（例如，`Point`、`Color`）。
    ```csharp
    public struct Point
    {
        public int X;
        public int Y;

        public Point(int x, int y)
        {
            X = x;
            Y = y;
        }
    }

    Point p1 = new Point(10, 20);
    Point p2 = p1; // p2 是 p1 的一个副本，修改 p2 不影响 p1
    p2.X = 5;
    Console.WriteLine($"p1: ({p1.X}, {p1.Y}), p2: ({p2.X}, {p2.Y})"); // p1: (10, 20), p2: (5, 20)
    ```

7.  **可空值类型 (Nullable Value Types):**
    *   `T?`: 允许值类型变量存储 `null`。例如 `int?`, `DateTime?`。

    **使用场景：** 数据库字段可能为空、可选参数等。
    ```csharp
    int? nullableInt = null;
    nullableInt = 123;
    Console.WriteLine(nullableInt.HasValue); // True
    Console.WriteLine(nullableInt.Value);    // 123

    DateTime? birthDate = null;
    birthDate = new DateTime(1990, 5, 15);
    ```

---

### 二、引用类型 (Reference Types)

引用类型变量不直接存储它们的值，而是存储对值的引用（内存地址）。当您将一个引用类型变量赋给另一个变量时，两个变量将引用内存中的同一个对象。它们通常存储在堆 (Heap) 上。

**主要特点：**
*   存储的是对象在内存中的地址（引用）。
*   赋值时是引用的拷贝，两个变量指向同一个对象。
*   通常存储在堆上。
*   派生自 `System.Object`。

**常见引用类型：**

1.  **字符串类型 (String Type):**
    *   `string`: 用于存储文本。尽管 `string` 是一个类 (`System.String`)，但在 C# 中它被赋予了特殊的地位，可以直接用字面量赋值。字符串是**不可变**的。

    **使用场景：** 姓名、地址、消息、任何文本数据。
    ```csharp
    string name = "Alice";
    string message = "Hello, " + name + "!";
    Console.WriteLine(message); // Hello, Alice!

    // 字符串不可变性示例
    string s1 = "world";
    string s2 = "Hello " + s1; // s2 是一个新的字符串对象，s1 保持不变
    ```

2.  **类类型 (Class Types):**
    *   `class`: 用户自定义的引用类型，是面向对象编程的基础。可以包含字段、方法、属性、事件等。

    **使用场景：** 几乎所有复杂的业务对象（客户、订单、产品等）。
    ```csharp
    public class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }

        public void Greet()
        {
            Console.WriteLine($"Hello, my name is {Name} and I am {Age} years old.");
        }
    }

    Person person1 = new Person { Name = "Bob", Age = 25 };
    Person person2 = person1; // person2 和 person1 引用同一个 Person 对象
    person2.Age = 26; // 修改 person2 也会影响 person1

    Console.WriteLine(person1.Age); // 26
    person1.Greet(); // Hello, my name is Bob and I am 26 years old.
    ```

3.  **接口类型 (Interface Types):**
    *   `interface`: 定义了一组契约（方法、属性、事件等），实现该接口的类或结构体必须提供这些成员的实现。

    **使用场景：** 定义行为规范、实现多态、解耦。
    ```carp
    public interface ILogger
    {
        void Log(string message);
    }

    public class ConsoleLogger : ILogger
    {
        public void Log(string message)
        {
            Console.WriteLine($"[LOG] {message}");
        }
    }

    ILogger logger = new ConsoleLogger();
    logger.Log("This is a test message.");
    ```

4.  **委托类型 (Delegate Types):**
    *   `delegate`: 类似于 C/C++ 中的函数指针，用于封装方法。是事件的基础。

    **使用场景：** 事件处理、回调函数、LINQ 查询。
    ```csharp
    public delegate void MyDelegate(string msg);

    public class Messenger
    {
        public void SendMessage(string message)
        {
            Console.WriteLine($"Sending: {message}");
        }
    }

    MyDelegate del = new Messenger().SendMessage;
    del("Hello from delegate!");
    ```

5.  **数组类型 (Array Types):**
    *   `T[]`: 可以存储相同类型元素的固定大小的集合。数组本身是引用类型，但它可以存储值类型或引用类型的元素。

    **使用场景：** 存储同类型数据的有序集合。
    ```csharp
    int[] numbers = new int[3]; // 存储值类型 int 的数组
    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;

    string[] names = { "Alice", "Bob", "Charlie" }; // 存储引用类型 string 的数组
    ```

6.  **`object` 类型 (Object Type):**
    *   `object`: `System.Object` 的别名，是所有 C# 类型的最终基类（包括值类型和引用类型）。它可以引用任何类型的数据。

    **使用场景：** 当你需要处理未知类型的数据时（但通常应避免过度使用，因为它会涉及装箱/拆箱操作，影响性能）。
    ```csharp
    object obj1 = 123; // int 被装箱 (boxing) 成 object
    object obj2 = "Hello"; // string 作为 object
    object obj3 = new Person(); // Person 对象作为 object

    int num = (int)obj1; // 拆箱 (unboxing) 回 int
    ```

---

### 三、隐式类型局部变量 (`var` 关键字)

C# 3.0 引入了 `var` 关键字，允许编译器根据初始化表达式推断变量的类型。这并不是一种新的数据类型，而是一种语法糖，编译器在编译时会替换为实际的类型。

**使用场景：** 简化代码，尤其是在匿名类型、LINQ 查询或类型名称很长时。
```csharp
var age = 30;           // 编译器推断为 int
var name = "David";     // 编译器推断为 string
var isActive = true;    // 编译器推断为 bool
var numbers = new List<int> { 1, 2, 3 }; // 编译器推断为 List<int>

// 注意：var 必须在声明时初始化，且不能用于字段或方法参数。
// var 并不是动态类型，它在编译时就已经确定了类型。
```

---

### 四、类型转换 (Type Conversion)

在 C# 中，不同数据类型之间可以进行转换。

1.  **隐式转换 (Implicit Conversion):**
    *   从较小范围的类型到较大范围的类型，不会丢失数据。编译器会自动执行。
    ```csharp
    int myInt = 100;
    long myLong = myInt; // int 隐式转换为 long
    float myFloat = myInt; // int 隐式转换为 float
    ```

2.  **显式转换 (Explicit Conversion / Casting):**
    *   从较大范围的类型到较小范围的类型，或可能丢失数据的转换。需要使用强制转换运算符 `()`。
    ```csharp
    double myDouble = 123.45;
    int myInt = (int)myDouble; // double 显式转换为 int，小数部分被截断，myInt 为 123

    long largeLong = 2_000_000_000_000L;
    int smallInt = (int)largeLong; // 显式转换为 int，可能导致数据溢出或丢失
    ```

3.  **使用 `Convert` 类：**
    *   `System.Convert` 类提供了多种静态方法，用于在基本数据类型之间进行转换，并能处理 `null` 值。
    ```csharp
    string strNum = "123";
    int num = Convert.ToInt32(strNum);

    double dValue = 98.76;
    string sValue = Convert.ToString(dValue);
    ```

4.  **`Parse()` 和 `TryParse()` 方法：**
    *   大多数基本类型（如 `int`, `double`, `DateTime`）都有 `Parse()` 和 `TryParse()` 方法，用于将字符串转换为该类型。
    *   `Parse()`：如果转换失败会抛出异常。
    *   `TryParse()`：如果转换失败会返回 `false`，不会抛出异常，更安全。
    ```csharp
    string s1 = "123";
    int i1 = int.Parse(s1); // i1 = 123

    string s2 = "abc";
    int i2;
    if (int.TryParse(s2, out i2))
    {
        Console.WriteLine($"转换成功: {i2}");
    }
    else
    {
        Console.WriteLine("转换失败"); // 输出：转换失败
    }
    ```

---

### 总结与最佳实践

*   **选择合适的数据类型：** 根据数据本身的特性（整数、小数、文本、布尔值）和其范围、精度要求来选择最合适的数据类型。
    *   **整数：** `int` 是最常用的，如果超出范围考虑 `long`。
    *   **小数：** 大多数情况用 `double`，**涉及金钱必须用 `decimal`**。
    *   **文本：** `string`。
    *   **布尔：** `bool`。
    *   **单个字符：** `char`。
    *   **有限状态：** `enum`。
    *   **轻量级数据结构：** `struct`。
    *   **复杂业务对象：** `class`。
    *   **可能为 `null` 的值类型：** `T?` (可空值类型)。

*   **理解值类型和引用类型的区别：** 这是 C# 中非常核心的概念，影响变量的赋值、方法的参数传递以及内存管理。
    *   值类型是“复制值”，引用类型是“复制引用”。

*   **注意类型转换：** 隐式转换是安全的，显式转换可能导致数据丢失或溢出，应谨慎使用。使用 `TryParse()` 进行字符串到数字的转换通常比 `Parse()` 更安全。

*   **善用 `var`：** 提高代码可读性和简洁性，但不要滥用，确保类型意图清晰。

通过理解和正确使用这些数据类型，您可以编写出高效、健壮且易于维护的 C# 代码。

