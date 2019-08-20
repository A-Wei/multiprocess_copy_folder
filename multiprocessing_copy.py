import os
import multiprocessing


def copy_file(q, file_name, copy_folder_name, new_folder_name):
    copy_f = open(copy_folder_name + "/" + file_name, "rb")
    content = copy_f.read()
    copy_f.close()

    new_f = open(new_folder_name + "/" + file_name, "wb")
    new_f.write(content)
    new_f.close()

    q.put(file_name)

def main():
    # 1. Get the folder name to copy
    copy_folder_name = input("Please give the name of folder you want to copy: ")

    # 2. Create a new folder
    try:
        new_folder_name = copy_folder_name + "_copy"
        os.mkdir(new_folder_name)
    except:
        pass

    # 3. Fetch all files in folder
    file_names = os.listdir(copy_folder_name)

    # 4. Create a multiprocessing pool
    po = multiprocessing.Pool(5)

    # 5. Create a queue (To be able to calculate the %)
    q = multiprocessing.Manager().Queue()

    # 6.Create copy job into pool
    for file_name in file_names:
        po.apply_async(copy_file, args=(q, file_name, copy_folder_name, new_folder_name))

    po.close()
    # po.join()
    all_file_num = len(file_names)
    copy_ok_num = 0

    while True:
        file_name = q.get()
        # print(f"Copy complete: {file_name}")
        copy_ok_num += 1

        # carriaga_return and end="" are necessary to be able to show only 1 line
        # carriage_return will move the curse to the begining of the line
        # end= is default to \n (new_line), only when we replace it with "", carriage_return
        # will work.
        carriage_return = "\r"
        print(f"{carriage_return}Copy Progress Rate: {int(copy_ok_num*100/all_file_num)}", end="")
        # print("\r拷贝的进度为: %.2f %%" % (copy_ok_num*100/all_file_num), end="")
        if copy_ok_num >= all_file_num:
            break


if __name__ == "__main__":
    main()
