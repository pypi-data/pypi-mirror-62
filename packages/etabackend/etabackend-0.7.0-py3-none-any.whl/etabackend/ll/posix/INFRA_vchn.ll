; ModuleID = 'etabackend/cpp/INFRA_vchn.cpp'
source_filename = "etabackend/cpp/INFRA_vchn.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.circular_buf_t = type { i64*, i64, i64, i64 }
%struct.VCHN_t = type { i8, i8, i8, i8, i32, i64*, i8*, %struct.circular_buf_t* }

@controlflow_guarantee = dso_local global i64 0, align 8
@.str = private unnamed_addr constant [52 x i8] c"\0A [ERROR]Memalloc failed for this VFILE, aborting.\0A\00", align 1
@.str.1 = private unnamed_addr constant [52 x i8] c"\0ACreating ring buffer %llx at %llx with size %lld. \00", align 1
@.str.2 = private unnamed_addr constant [53 x i8] c"\0AResetting ring buffer %llx at %llx with size %lld. \00", align 1
@.str.3 = private unnamed_addr constant [37 x i8] c"\0A [ERROR]Memalloc failed, aborting.\0A\00", align 1
@.str.4 = private unnamed_addr constant [14 x i8] c"\0APOOL_init %d\00", align 1
@.str.5 = private unnamed_addr constant [22 x i8] c"\0APOOL_init resumed %d\00", align 1
@.str.6 = private unnamed_addr constant [40 x i8] c"\0AVCHN_RFILES: %d,VCHN_VFILES_offset:%d \00", align 1
@.str.7 = private unnamed_addr constant [54 x i8] c"\0A [ERROR]Memalloc failed for VFILES index, aborting.\0A\00", align 1
@.str.8 = private unnamed_addr constant [34 x i8] c"\0A [FATAL]Buffer overflow! at %llx\00", align 1

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @circular_buf_reset(%struct.circular_buf_t*) #0 {
  %2 = alloca %struct.circular_buf_t*, align 8
  %3 = alloca i32, align 4
  store %struct.circular_buf_t* %0, %struct.circular_buf_t** %2, align 8
  store i32 -1, i32* %3, align 4
  %4 = load %struct.circular_buf_t*, %struct.circular_buf_t** %2, align 8
  %5 = icmp ne %struct.circular_buf_t* %4, null
  br i1 %5, label %6, label %11

; <label>:6:                                      ; preds = %1
  %7 = load %struct.circular_buf_t*, %struct.circular_buf_t** %2, align 8
  %8 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %7, i32 0, i32 1
  store i64 0, i64* %8, align 8
  %9 = load %struct.circular_buf_t*, %struct.circular_buf_t** %2, align 8
  %10 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %9, i32 0, i32 2
  store i64 0, i64* %10, align 8
  store i32 0, i32* %3, align 4
  br label %11

; <label>:11:                                     ; preds = %6, %1
  %12 = load i32, i32* %3, align 4
  ret i32 %12
}

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @circular_buf_put(%struct.circular_buf_t*, i64) #0 {
  %3 = alloca %struct.circular_buf_t*, align 8
  %4 = alloca i64, align 8
  %5 = alloca i32, align 4
  store %struct.circular_buf_t* %0, %struct.circular_buf_t** %3, align 8
  store i64 %1, i64* %4, align 8
  store i32 -1, i32* %5, align 4
  %6 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %7 = icmp ne %struct.circular_buf_t* %6, null
  br i1 %7, label %8, label %46

; <label>:8:                                      ; preds = %2
  %9 = load i64, i64* %4, align 8
  %10 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %11 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %10, i32 0, i32 0
  %12 = load i64*, i64** %11, align 8
  %13 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %14 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %13, i32 0, i32 1
  %15 = load i64, i64* %14, align 8
  %16 = getelementptr inbounds i64, i64* %12, i64 %15
  store i64 %9, i64* %16, align 8
  %17 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %18 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %17, i32 0, i32 1
  %19 = load i64, i64* %18, align 8
  %20 = add nsw i64 %19, 1
  %21 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %22 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %21, i32 0, i32 3
  %23 = load i64, i64* %22, align 8
  %24 = srem i64 %20, %23
  %25 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %26 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %25, i32 0, i32 1
  store i64 %24, i64* %26, align 8
  %27 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %28 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %27, i32 0, i32 1
  %29 = load i64, i64* %28, align 8
  %30 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %31 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %30, i32 0, i32 2
  %32 = load i64, i64* %31, align 8
  %33 = icmp eq i64 %29, %32
  br i1 %33, label %34, label %45

; <label>:34:                                     ; preds = %8
  %35 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %36 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %35, i32 0, i32 2
  %37 = load i64, i64* %36, align 8
  %38 = add nsw i64 %37, 1
  %39 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %40 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %39, i32 0, i32 3
  %41 = load i64, i64* %40, align 8
  %42 = srem i64 %38, %41
  %43 = load %struct.circular_buf_t*, %struct.circular_buf_t** %3, align 8
  %44 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %43, i32 0, i32 2
  store i64 %42, i64* %44, align 8
  br label %45

; <label>:45:                                     ; preds = %34, %8
  store i32 0, i32* %5, align 4
  br label %46

; <label>:46:                                     ; preds = %45, %2
  %47 = load i32, i32* %5, align 4
  ret i32 %47
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @circular_buf_get(%struct.circular_buf_t*, i64*, i1 zeroext) #1 {
  %4 = alloca %struct.circular_buf_t, align 8
  %5 = alloca %struct.circular_buf_t*, align 8
  %6 = alloca i64*, align 8
  %7 = alloca i8, align 1
  %8 = alloca i32, align 4
  %9 = alloca %struct.circular_buf_t, align 8
  store %struct.circular_buf_t* %0, %struct.circular_buf_t** %5, align 8
  store i64* %1, i64** %6, align 8
  %10 = zext i1 %2 to i8
  store i8 %10, i8* %7, align 1
  store i32 -1, i32* %8, align 4
  %11 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %12 = icmp ne %struct.circular_buf_t* %11, null
  br i1 %12, label %13, label %51

; <label>:13:                                     ; preds = %3
  %14 = load i64*, i64** %6, align 8
  %15 = icmp ne i64* %14, null
  br i1 %15, label %16, label %51

; <label>:16:                                     ; preds = %13
  %17 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %18 = bitcast %struct.circular_buf_t* %9 to i8*
  %19 = bitcast %struct.circular_buf_t* %17 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %18, i8* align 8 %19, i64 32, i1 false)
  %20 = bitcast %struct.circular_buf_t* %4 to i8*
  %21 = bitcast %struct.circular_buf_t* %9 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %20, i8* align 1 %21, i64 32, i1 false)
  %22 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %4, i32 0, i32 1
  %23 = load i64, i64* %22, align 8
  %24 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %4, i32 0, i32 2
  %25 = load i64, i64* %24, align 8
  %26 = icmp eq i64 %23, %25
  br i1 %26, label %51, label %27

; <label>:27:                                     ; preds = %16
  %28 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %29 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %28, i32 0, i32 0
  %30 = load i64*, i64** %29, align 8
  %31 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %32 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %31, i32 0, i32 2
  %33 = load i64, i64* %32, align 8
  %34 = getelementptr inbounds i64, i64* %30, i64 %33
  %35 = load i64, i64* %34, align 8
  %36 = load i64*, i64** %6, align 8
  store i64 %35, i64* %36, align 8
  %37 = load i8, i8* %7, align 1
  %38 = trunc i8 %37 to i1
  br i1 %38, label %39, label %50

; <label>:39:                                     ; preds = %27
  %40 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %41 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %40, i32 0, i32 2
  %42 = load i64, i64* %41, align 8
  %43 = add nsw i64 %42, 1
  %44 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %45 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %44, i32 0, i32 3
  %46 = load i64, i64* %45, align 8
  %47 = srem i64 %43, %46
  %48 = load %struct.circular_buf_t*, %struct.circular_buf_t** %5, align 8
  %49 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %48, i32 0, i32 2
  store i64 %47, i64* %49, align 8
  br label %50

; <label>:50:                                     ; preds = %39, %27
  store i32 0, i32* %8, align 4
  br label %51

; <label>:51:                                     ; preds = %50, %16, %13, %3
  %52 = load i32, i32* %8, align 4
  ret i32 %52
}

; Function Attrs: alwaysinline nounwind uwtable
define dso_local zeroext i1 @circular_buf_empty(%struct.circular_buf_t* byval align 8) #0 {
  %2 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %0, i32 0, i32 1
  %3 = load i64, i64* %2, align 8
  %4 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %0, i32 0, i32 2
  %5 = load i64, i64* %4, align 8
  %6 = icmp eq i64 %3, %5
  ret i1 %6
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i1) #2

; Function Attrs: alwaysinline nounwind uwtable
define dso_local zeroext i1 @circular_buf_full(%struct.circular_buf_t* byval align 8) #0 {
  %2 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %0, i32 0, i32 1
  %3 = load i64, i64* %2, align 8
  %4 = add nsw i64 %3, 1
  %5 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %0, i32 0, i32 3
  %6 = load i64, i64* %5, align 8
  %7 = srem i64 %4, %6
  %8 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %0, i32 0, i32 2
  %9 = load i64, i64* %8, align 8
  %10 = icmp eq i64 %7, %9
  ret i1 %10
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @VFILE_init(%struct.VCHN_t*, i64, i64, i8*, i64) #1 {
  %6 = alloca %struct.circular_buf_t*, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca %struct.VCHN_t*, align 8
  %10 = alloca i64, align 8
  %11 = alloca i64, align 8
  %12 = alloca i8*, align 8
  %13 = alloca i64, align 8
  store %struct.VCHN_t* %0, %struct.VCHN_t** %9, align 8
  store i64 %1, i64* %10, align 8
  store i64 %2, i64* %11, align 8
  store i8* %3, i8** %12, align 8
  store i64 %4, i64* %13, align 8
  %14 = load i8*, i8** %12, align 8
  %15 = bitcast i8* %14 to i64*
  %16 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %17 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %16, i32 0, i32 7
  %18 = load %struct.circular_buf_t*, %struct.circular_buf_t** %17, align 8
  %19 = load i64, i64* %10, align 8
  %20 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %18, i64 %19
  %21 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %20, i32 0, i32 0
  store i64* %15, i64** %21, align 8
  %22 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %23 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %22, i32 0, i32 7
  %24 = load %struct.circular_buf_t*, %struct.circular_buf_t** %23, align 8
  %25 = load i64, i64* %10, align 8
  %26 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %24, i64 %25
  %27 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %26, i32 0, i32 0
  %28 = load i64*, i64** %27, align 8
  %29 = icmp eq i64* %28, null
  br i1 %29, label %30, label %33

; <label>:30:                                     ; preds = %5
  %31 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([52 x i8], [52 x i8]* @.str, i32 0, i32 0))
  %32 = sext i32 %31 to i64
  store i64 %32, i64* @controlflow_guarantee, align 8
  store i32 -1, i32* %8, align 4
  br label %84

; <label>:33:                                     ; preds = %5
  %34 = load i64, i64* %13, align 8
  %35 = icmp eq i64 %34, 1
  br i1 %35, label %36, label %70

; <label>:36:                                     ; preds = %33
  %37 = load i64, i64* %11, align 8
  %38 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %39 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %38, i32 0, i32 7
  %40 = load %struct.circular_buf_t*, %struct.circular_buf_t** %39, align 8
  %41 = load i64, i64* %10, align 8
  %42 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %40, i64 %41
  %43 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %42, i32 0, i32 3
  store i64 %37, i64* %43, align 8
  %44 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %45 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %44, i32 0, i32 7
  %46 = load %struct.circular_buf_t*, %struct.circular_buf_t** %45, align 8
  %47 = load i64, i64* %10, align 8
  %48 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %46, i64 %47
  store %struct.circular_buf_t* %48, %struct.circular_buf_t** %6, align 8
  store i32 -1, i32* %7, align 4
  %49 = load %struct.circular_buf_t*, %struct.circular_buf_t** %6, align 8
  %50 = icmp ne %struct.circular_buf_t* %49, null
  br i1 %50, label %51, label %56

; <label>:51:                                     ; preds = %36
  %52 = load %struct.circular_buf_t*, %struct.circular_buf_t** %6, align 8
  %53 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %52, i32 0, i32 1
  store i64 0, i64* %53, align 8
  %54 = load %struct.circular_buf_t*, %struct.circular_buf_t** %6, align 8
  %55 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %54, i32 0, i32 2
  store i64 0, i64* %55, align 8
  store i32 0, i32* %7, align 4
  br label %56

; <label>:56:                                     ; preds = %36, %51
  %57 = load i32, i32* %7, align 4
  %58 = load i64, i64* %10, align 8
  %59 = load i8*, i8** %12, align 8
  %60 = ptrtoint i8* %59 to i64
  %61 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %62 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %61, i32 0, i32 7
  %63 = load %struct.circular_buf_t*, %struct.circular_buf_t** %62, align 8
  %64 = load i64, i64* %10, align 8
  %65 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %63, i64 %64
  %66 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %65, i32 0, i32 3
  %67 = load i64, i64* %66, align 8
  %68 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([52 x i8], [52 x i8]* @.str.1, i32 0, i32 0), i64 %58, i64 %60, i64 %67)
  %69 = sext i32 %68 to i64
  store i64 %69, i64* @controlflow_guarantee, align 8
  br label %83

; <label>:70:                                     ; preds = %33
  %71 = load i64, i64* %10, align 8
  %72 = load i8*, i8** %12, align 8
  %73 = ptrtoint i8* %72 to i64
  %74 = load %struct.VCHN_t*, %struct.VCHN_t** %9, align 8
  %75 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %74, i32 0, i32 7
  %76 = load %struct.circular_buf_t*, %struct.circular_buf_t** %75, align 8
  %77 = load i64, i64* %10, align 8
  %78 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %76, i64 %77
  %79 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %78, i32 0, i32 3
  %80 = load i64, i64* %79, align 8
  %81 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @.str.2, i32 0, i32 0), i64 %71, i64 %73, i64 %80)
  %82 = sext i32 %81 to i64
  store i64 %82, i64* @controlflow_guarantee, align 8
  br label %83

; <label>:83:                                     ; preds = %70, %56
  store i32 0, i32* %8, align 4
  br label %84

; <label>:84:                                     ; preds = %83, %30
  %85 = load i32, i32* %8, align 4
  ret i32 %85
}

declare dso_local i32 @printf(i8*, ...) #3

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @POOL_update(%struct.VCHN_t*, i64, i8 zeroext) #0 {
  %4 = alloca %struct.VCHN_t*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i8, align 1
  %7 = alloca i8, align 1
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca i8, align 1
  store %struct.VCHN_t* %0, %struct.VCHN_t** %4, align 8
  store i64 %1, i64* %5, align 8
  store i8 %2, i8* %6, align 1
  %11 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %12 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %11, i32 0, i32 2
  %13 = load i8, i8* %12, align 2
  %14 = zext i8 %13 to i32
  %15 = load i8, i8* %6, align 1
  %16 = zext i8 %15 to i32
  %17 = add nsw i32 %14, %16
  %18 = trunc i32 %17 to i8
  store i8 %18, i8* %7, align 1
  %19 = load i64, i64* %5, align 8
  %20 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %21 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %20, i32 0, i32 5
  %22 = load i64*, i64** %21, align 8
  %23 = load i8, i8* %7, align 1
  %24 = zext i8 %23 to i64
  %25 = getelementptr inbounds i64, i64* %22, i64 %24
  store i64 %19, i64* %25, align 8
  %26 = load i8, i8* %6, align 1
  %27 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %28 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %27, i32 0, i32 6
  %29 = load i8*, i8** %28, align 8
  %30 = load i8, i8* %7, align 1
  %31 = zext i8 %30 to i64
  %32 = getelementptr inbounds i8, i8* %29, i64 %31
  store i8 %26, i8* %32, align 1
  br label %33

; <label>:33:                                     ; preds = %123, %3
  %34 = load i8, i8* %7, align 1
  %35 = zext i8 %34 to i32
  %36 = icmp sgt i32 %35, 0
  br i1 %36, label %37, label %125

; <label>:37:                                     ; preds = %33
  %38 = load i8, i8* %7, align 1
  %39 = zext i8 %38 to i32
  %40 = sub nsw i32 %39, 1
  %41 = sdiv i32 %40, 2
  %42 = trunc i32 %41 to i8
  store i8 %42, i8* %8, align 1
  %43 = load i8, i8* %8, align 1
  %44 = zext i8 %43 to i32
  %45 = add nsw i32 %44, 1
  %46 = mul nsw i32 %45, 2
  %47 = sub nsw i32 %46, 1
  %48 = trunc i32 %47 to i8
  store i8 %48, i8* %9, align 1
  %49 = load i8, i8* %8, align 1
  %50 = zext i8 %49 to i32
  %51 = add nsw i32 %50, 1
  %52 = mul nsw i32 %51, 2
  %53 = trunc i32 %52 to i8
  store i8 %53, i8* %10, align 1
  %54 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %55 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %54, i32 0, i32 5
  %56 = load i64*, i64** %55, align 8
  %57 = load i8, i8* %9, align 1
  %58 = zext i8 %57 to i64
  %59 = getelementptr inbounds i64, i64* %56, i64 %58
  %60 = load i64, i64* %59, align 8
  %61 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %62 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %61, i32 0, i32 5
  %63 = load i64*, i64** %62, align 8
  %64 = load i8, i8* %10, align 1
  %65 = zext i8 %64 to i64
  %66 = getelementptr inbounds i64, i64* %63, i64 %65
  %67 = load i64, i64* %66, align 8
  %68 = icmp slt i64 %60, %67
  br i1 %68, label %69, label %96

; <label>:69:                                     ; preds = %37
  %70 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %71 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %70, i32 0, i32 5
  %72 = load i64*, i64** %71, align 8
  %73 = load i8, i8* %9, align 1
  %74 = zext i8 %73 to i64
  %75 = getelementptr inbounds i64, i64* %72, i64 %74
  %76 = load i64, i64* %75, align 8
  %77 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %78 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %77, i32 0, i32 5
  %79 = load i64*, i64** %78, align 8
  %80 = load i8, i8* %8, align 1
  %81 = zext i8 %80 to i64
  %82 = getelementptr inbounds i64, i64* %79, i64 %81
  store i64 %76, i64* %82, align 8
  %83 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %84 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %83, i32 0, i32 6
  %85 = load i8*, i8** %84, align 8
  %86 = load i8, i8* %9, align 1
  %87 = zext i8 %86 to i64
  %88 = getelementptr inbounds i8, i8* %85, i64 %87
  %89 = load i8, i8* %88, align 1
  %90 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %91 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %90, i32 0, i32 6
  %92 = load i8*, i8** %91, align 8
  %93 = load i8, i8* %8, align 1
  %94 = zext i8 %93 to i64
  %95 = getelementptr inbounds i8, i8* %92, i64 %94
  store i8 %89, i8* %95, align 1
  br label %123

; <label>:96:                                     ; preds = %37
  %97 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %98 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %97, i32 0, i32 5
  %99 = load i64*, i64** %98, align 8
  %100 = load i8, i8* %10, align 1
  %101 = zext i8 %100 to i64
  %102 = getelementptr inbounds i64, i64* %99, i64 %101
  %103 = load i64, i64* %102, align 8
  %104 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %105 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %104, i32 0, i32 5
  %106 = load i64*, i64** %105, align 8
  %107 = load i8, i8* %8, align 1
  %108 = zext i8 %107 to i64
  %109 = getelementptr inbounds i64, i64* %106, i64 %108
  store i64 %103, i64* %109, align 8
  %110 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %111 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %110, i32 0, i32 6
  %112 = load i8*, i8** %111, align 8
  %113 = load i8, i8* %10, align 1
  %114 = zext i8 %113 to i64
  %115 = getelementptr inbounds i8, i8* %112, i64 %114
  %116 = load i8, i8* %115, align 1
  %117 = load %struct.VCHN_t*, %struct.VCHN_t** %4, align 8
  %118 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %117, i32 0, i32 6
  %119 = load i8*, i8** %118, align 8
  %120 = load i8, i8* %8, align 1
  %121 = zext i8 %120 to i64
  %122 = getelementptr inbounds i8, i8* %119, i64 %121
  store i8 %116, i8* %122, align 1
  br label %123

; <label>:123:                                    ; preds = %96, %69
  %124 = load i8, i8* %8, align 1
  store i8 %124, i8* %7, align 1
  br label %33

; <label>:125:                                    ; preds = %33
  ret i32 0
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @POOL_init(%struct.VCHN_t*, i64, i64, i8*, i8*, i64) #1 {
  %7 = alloca i32, align 4
  %8 = alloca %struct.VCHN_t*, align 8
  %9 = alloca i64, align 8
  %10 = alloca i64, align 8
  %11 = alloca i8*, align 8
  %12 = alloca i8*, align 8
  %13 = alloca i64, align 8
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  store %struct.VCHN_t* %0, %struct.VCHN_t** %8, align 8
  store i64 %1, i64* %9, align 8
  store i64 %2, i64* %10, align 8
  store i8* %3, i8** %11, align 8
  store i8* %4, i8** %12, align 8
  store i64 %5, i64* %13, align 8
  %16 = load i64, i64* %9, align 8
  %17 = trunc i64 %16 to i8
  %18 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %19 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %18, i32 0, i32 2
  store i8 %17, i8* %19, align 2
  %20 = load i8*, i8** %11, align 8
  %21 = bitcast i8* %20 to i64*
  %22 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %23 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %22, i32 0, i32 5
  store i64* %21, i64** %23, align 8
  %24 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %25 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %24, i32 0, i32 5
  %26 = load i64*, i64** %25, align 8
  %27 = icmp eq i64* %26, null
  br i1 %27, label %28, label %31

; <label>:28:                                     ; preds = %6
  %29 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([37 x i8], [37 x i8]* @.str.3, i32 0, i32 0))
  %30 = sext i32 %29 to i64
  store i64 %30, i64* @controlflow_guarantee, align 8
  store i32 -1, i32* %7, align 4
  br label %107

; <label>:31:                                     ; preds = %6
  %32 = load i8*, i8** %12, align 8
  %33 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %34 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %33, i32 0, i32 6
  store i8* %32, i8** %34, align 8
  %35 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %36 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %35, i32 0, i32 6
  %37 = load i8*, i8** %36, align 8
  %38 = icmp eq i8* %37, null
  br i1 %38, label %39, label %42

; <label>:39:                                     ; preds = %31
  %40 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([37 x i8], [37 x i8]* @.str.3, i32 0, i32 0))
  %41 = sext i32 %40 to i64
  store i64 %41, i64* @controlflow_guarantee, align 8
  store i32 -1, i32* %7, align 4
  br label %107

; <label>:42:                                     ; preds = %31
  %43 = load i64, i64* %13, align 8
  %44 = icmp eq i64 %43, 0
  br i1 %44, label %45, label %99

; <label>:45:                                     ; preds = %42
  %46 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %47 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %46, i32 0, i32 2
  %48 = load i8, i8* %47, align 2
  %49 = zext i8 %48 to i32
  %50 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.4, i32 0, i32 0), i32 %49)
  %51 = sext i32 %50 to i64
  store i64 %51, i64* @controlflow_guarantee, align 8
  store i32 0, i32* %14, align 4
  br label %52

; <label>:52:                                     ; preds = %70, %45
  %53 = load i32, i32* %14, align 4
  %54 = sext i32 %53 to i64
  %55 = load i64, i64* %10, align 8
  %56 = icmp slt i64 %54, %55
  br i1 %56, label %57, label %73

; <label>:57:                                     ; preds = %52
  %58 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %59 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %58, i32 0, i32 5
  %60 = load i64*, i64** %59, align 8
  %61 = load i32, i32* %14, align 4
  %62 = sext i32 %61 to i64
  %63 = getelementptr inbounds i64, i64* %60, i64 %62
  store i64 9223372036854775807, i64* %63, align 8
  %64 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %65 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %64, i32 0, i32 6
  %66 = load i8*, i8** %65, align 8
  %67 = load i32, i32* %14, align 4
  %68 = sext i32 %67 to i64
  %69 = getelementptr inbounds i8, i8* %66, i64 %68
  store i8 0, i8* %69, align 1
  br label %70

; <label>:70:                                     ; preds = %57
  %71 = load i32, i32* %14, align 4
  %72 = add nsw i32 %71, 1
  store i32 %72, i32* %14, align 4
  br label %52

; <label>:73:                                     ; preds = %52
  store i32 0, i32* %15, align 4
  br label %74

; <label>:74:                                     ; preds = %95, %73
  %75 = load i32, i32* %15, align 4
  %76 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %77 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %76, i32 0, i32 2
  %78 = load i8, i8* %77, align 2
  %79 = zext i8 %78 to i32
  %80 = icmp slt i32 %75, %79
  br i1 %80, label %81, label %98

; <label>:81:                                     ; preds = %74
  %82 = load i32, i32* %15, align 4
  %83 = trunc i32 %82 to i8
  %84 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %85 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %84, i32 0, i32 6
  %86 = load i8*, i8** %85, align 8
  %87 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %88 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %87, i32 0, i32 2
  %89 = load i8, i8* %88, align 2
  %90 = zext i8 %89 to i32
  %91 = load i32, i32* %15, align 4
  %92 = add nsw i32 %90, %91
  %93 = sext i32 %92 to i64
  %94 = getelementptr inbounds i8, i8* %86, i64 %93
  store i8 %83, i8* %94, align 1
  br label %95

; <label>:95:                                     ; preds = %81
  %96 = load i32, i32* %15, align 4
  %97 = add nsw i32 %96, 1
  store i32 %97, i32* %15, align 4
  br label %74

; <label>:98:                                     ; preds = %74
  br label %106

; <label>:99:                                     ; preds = %42
  %100 = load %struct.VCHN_t*, %struct.VCHN_t** %8, align 8
  %101 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %100, i32 0, i32 2
  %102 = load i8, i8* %101, align 2
  %103 = zext i8 %102 to i32
  %104 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([22 x i8], [22 x i8]* @.str.5, i32 0, i32 0), i32 %103)
  %105 = sext i32 %104 to i64
  store i64 %105, i64* @controlflow_guarantee, align 8
  br label %106

; <label>:106:                                    ; preds = %99, %98
  store i32 0, i32* %7, align 4
  br label %107

; <label>:107:                                    ; preds = %106, %39, %28
  %108 = load i32, i32* %7, align 4
  ret i32 %108
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @VCHN_init(%struct.VCHN_t*, i64, i64, i64, i8*) #1 {
  %6 = alloca i32, align 4
  %7 = alloca %struct.VCHN_t*, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  %10 = alloca i64, align 8
  %11 = alloca i8*, align 8
  store %struct.VCHN_t* %0, %struct.VCHN_t** %7, align 8
  store i64 %1, i64* %8, align 8
  store i64 %2, i64* %9, align 8
  store i64 %3, i64* %10, align 8
  store i8* %4, i8** %11, align 8
  %12 = load i64, i64* %8, align 8
  %13 = trunc i64 %12 to i8
  %14 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %15 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %14, i32 0, i32 1
  store i8 %13, i8* %15, align 1
  %16 = load i64, i64* %9, align 8
  %17 = trunc i64 %16 to i8
  %18 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %19 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %18, i32 0, i32 0
  store i8 %17, i8* %19, align 8
  %20 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %21 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %20, i32 0, i32 1
  %22 = load i8, i8* %21, align 1
  %23 = zext i8 %22 to i32
  %24 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %25 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %24, i32 0, i32 0
  %26 = load i8, i8* %25, align 8
  %27 = zext i8 %26 to i32
  %28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.6, i32 0, i32 0), i32 %23, i32 %27)
  %29 = sext i32 %28 to i64
  store i64 %29, i64* @controlflow_guarantee, align 8
  %30 = load i8*, i8** %11, align 8
  %31 = bitcast i8* %30 to %struct.circular_buf_t*
  %32 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %33 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %32, i32 0, i32 7
  store %struct.circular_buf_t* %31, %struct.circular_buf_t** %33, align 8
  %34 = load %struct.VCHN_t*, %struct.VCHN_t** %7, align 8
  %35 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %34, i32 0, i32 7
  %36 = load %struct.circular_buf_t*, %struct.circular_buf_t** %35, align 8
  %37 = icmp eq %struct.circular_buf_t* %36, null
  br i1 %37, label %38, label %41

; <label>:38:                                     ; preds = %5
  %39 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([54 x i8], [54 x i8]* @.str.7, i32 0, i32 0))
  %40 = sext i32 %39 to i64
  store i64 %40, i64* @controlflow_guarantee, align 8
  store i32 -1, i32* %6, align 4
  br label %42

; <label>:41:                                     ; preds = %5
  store i32 0, i32* %6, align 4
  br label %42

; <label>:42:                                     ; preds = %41, %38
  %43 = load i32, i32* %6, align 4
  ret i32 %43
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @VCHN_put(%struct.VCHN_t*, i64, i8 zeroext) #1 {
  %4 = alloca %struct.circular_buf_t*, align 8
  %5 = alloca i32, align 4
  %6 = alloca %struct.VCHN_t*, align 8
  %7 = alloca i64, align 8
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca i8, align 1
  %11 = alloca i8, align 1
  %12 = alloca i8, align 1
  %13 = alloca %struct.circular_buf_t, align 8
  %14 = alloca %struct.circular_buf_t*, align 8
  %15 = alloca i64, align 8
  %16 = alloca i32, align 4
  %17 = alloca %struct.VCHN_t*, align 8
  %18 = alloca i64, align 8
  %19 = alloca i8, align 1
  %20 = alloca i8, align 1
  %21 = alloca i8, align 1
  %22 = alloca i8, align 1
  %23 = alloca i8, align 1
  %24 = alloca i32, align 4
  %25 = alloca %struct.VCHN_t*, align 8
  %26 = alloca i64, align 8
  %27 = alloca i8, align 1
  %28 = alloca i32, align 4
  %29 = alloca i32, align 4
  %30 = alloca i8, align 1
  %31 = alloca i32, align 4
  %32 = alloca %struct.circular_buf_t, align 8
  %33 = alloca i32, align 4
  store %struct.VCHN_t* %0, %struct.VCHN_t** %25, align 8
  store i64 %1, i64* %26, align 8
  store i8 %2, i8* %27, align 1
  %34 = load i8, i8* %27, align 1
  %35 = zext i8 %34 to i32
  %36 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %37 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %36, i32 0, i32 0
  %38 = load i8, i8* %37, align 8
  %39 = zext i8 %38 to i32
  %40 = sub nsw i32 %35, %39
  store i32 %40, i32* %28, align 4
  %41 = load i32, i32* %28, align 4
  %42 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %43 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %42, i32 0, i32 1
  %44 = load i8, i8* %43, align 1
  %45 = zext i8 %44 to i32
  %46 = add nsw i32 %41, %45
  store i32 %46, i32* %29, align 4
  %47 = load i64, i64* %26, align 8
  %48 = icmp eq i64 %47, 9223372036854775807
  br i1 %48, label %49, label %184

; <label>:49:                                     ; preds = %3
  %50 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %51 = load i64, i64* %26, align 8
  %52 = load i32, i32* %29, align 4
  %53 = trunc i32 %52 to i8
  store %struct.VCHN_t* %50, %struct.VCHN_t** %17, align 8
  store i64 %51, i64* %18, align 8
  store i8 %53, i8* %19, align 1
  %54 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %55 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %54, i32 0, i32 2
  %56 = load i8, i8* %55, align 2
  %57 = zext i8 %56 to i32
  %58 = load i8, i8* %19, align 1
  %59 = zext i8 %58 to i32
  %60 = add nsw i32 %57, %59
  %61 = trunc i32 %60 to i8
  store i8 %61, i8* %20, align 1
  %62 = load i64, i64* %18, align 8
  %63 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %64 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %63, i32 0, i32 5
  %65 = load i64*, i64** %64, align 8
  %66 = load i8, i8* %20, align 1
  %67 = zext i8 %66 to i64
  %68 = getelementptr inbounds i64, i64* %65, i64 %67
  store i64 %62, i64* %68, align 8
  %69 = load i8, i8* %19, align 1
  %70 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %71 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %70, i32 0, i32 6
  %72 = load i8*, i8** %71, align 8
  %73 = load i8, i8* %20, align 1
  %74 = zext i8 %73 to i64
  %75 = getelementptr inbounds i8, i8* %72, i64 %74
  store i8 %69, i8* %75, align 1
  br label %76

; <label>:76:                                     ; preds = %166, %49
  %77 = load i8, i8* %20, align 1
  %78 = zext i8 %77 to i32
  %79 = icmp sgt i32 %78, 0
  br i1 %79, label %80, label %168

; <label>:80:                                     ; preds = %76
  %81 = load i8, i8* %20, align 1
  %82 = zext i8 %81 to i32
  %83 = sub nsw i32 %82, 1
  %84 = sdiv i32 %83, 2
  %85 = trunc i32 %84 to i8
  store i8 %85, i8* %21, align 1
  %86 = load i8, i8* %21, align 1
  %87 = zext i8 %86 to i32
  %88 = add nsw i32 %87, 1
  %89 = mul nsw i32 %88, 2
  %90 = sub nsw i32 %89, 1
  %91 = trunc i32 %90 to i8
  store i8 %91, i8* %22, align 1
  %92 = load i8, i8* %21, align 1
  %93 = zext i8 %92 to i32
  %94 = add nsw i32 %93, 1
  %95 = mul nsw i32 %94, 2
  %96 = trunc i32 %95 to i8
  store i8 %96, i8* %23, align 1
  %97 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %98 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %97, i32 0, i32 5
  %99 = load i64*, i64** %98, align 8
  %100 = load i8, i8* %22, align 1
  %101 = zext i8 %100 to i64
  %102 = getelementptr inbounds i64, i64* %99, i64 %101
  %103 = load i64, i64* %102, align 8
  %104 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %105 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %104, i32 0, i32 5
  %106 = load i64*, i64** %105, align 8
  %107 = load i8, i8* %23, align 1
  %108 = zext i8 %107 to i64
  %109 = getelementptr inbounds i64, i64* %106, i64 %108
  %110 = load i64, i64* %109, align 8
  %111 = icmp slt i64 %103, %110
  br i1 %111, label %112, label %139

; <label>:112:                                    ; preds = %80
  %113 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %114 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %113, i32 0, i32 5
  %115 = load i64*, i64** %114, align 8
  %116 = load i8, i8* %22, align 1
  %117 = zext i8 %116 to i64
  %118 = getelementptr inbounds i64, i64* %115, i64 %117
  %119 = load i64, i64* %118, align 8
  %120 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %121 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %120, i32 0, i32 5
  %122 = load i64*, i64** %121, align 8
  %123 = load i8, i8* %21, align 1
  %124 = zext i8 %123 to i64
  %125 = getelementptr inbounds i64, i64* %122, i64 %124
  store i64 %119, i64* %125, align 8
  %126 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %127 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %126, i32 0, i32 6
  %128 = load i8*, i8** %127, align 8
  %129 = load i8, i8* %22, align 1
  %130 = zext i8 %129 to i64
  %131 = getelementptr inbounds i8, i8* %128, i64 %130
  %132 = load i8, i8* %131, align 1
  %133 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %134 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %133, i32 0, i32 6
  %135 = load i8*, i8** %134, align 8
  %136 = load i8, i8* %21, align 1
  %137 = zext i8 %136 to i64
  %138 = getelementptr inbounds i8, i8* %135, i64 %137
  store i8 %132, i8* %138, align 1
  br label %166

; <label>:139:                                    ; preds = %80
  %140 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %141 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %140, i32 0, i32 5
  %142 = load i64*, i64** %141, align 8
  %143 = load i8, i8* %23, align 1
  %144 = zext i8 %143 to i64
  %145 = getelementptr inbounds i64, i64* %142, i64 %144
  %146 = load i64, i64* %145, align 8
  %147 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %148 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %147, i32 0, i32 5
  %149 = load i64*, i64** %148, align 8
  %150 = load i8, i8* %21, align 1
  %151 = zext i8 %150 to i64
  %152 = getelementptr inbounds i64, i64* %149, i64 %151
  store i64 %146, i64* %152, align 8
  %153 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %154 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %153, i32 0, i32 6
  %155 = load i8*, i8** %154, align 8
  %156 = load i8, i8* %23, align 1
  %157 = zext i8 %156 to i64
  %158 = getelementptr inbounds i8, i8* %155, i64 %157
  %159 = load i8, i8* %158, align 1
  %160 = load %struct.VCHN_t*, %struct.VCHN_t** %17, align 8
  %161 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %160, i32 0, i32 6
  %162 = load i8*, i8** %161, align 8
  %163 = load i8, i8* %21, align 1
  %164 = zext i8 %163 to i64
  %165 = getelementptr inbounds i8, i8* %162, i64 %164
  store i8 %159, i8* %165, align 1
  br label %166

; <label>:166:                                    ; preds = %139, %112
  %167 = load i8, i8* %21, align 1
  store i8 %167, i8* %20, align 1
  br label %76

; <label>:168:                                    ; preds = %76
  %169 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %170 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %169, i32 0, i32 7
  %171 = load %struct.circular_buf_t*, %struct.circular_buf_t** %170, align 8
  %172 = load i32, i32* %28, align 4
  %173 = sext i32 %172 to i64
  %174 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %171, i64 %173
  store %struct.circular_buf_t* %174, %struct.circular_buf_t** %4, align 8
  store i32 -1, i32* %5, align 4
  %175 = load %struct.circular_buf_t*, %struct.circular_buf_t** %4, align 8
  %176 = icmp ne %struct.circular_buf_t* %175, null
  br i1 %176, label %177, label %182

; <label>:177:                                    ; preds = %168
  %178 = load %struct.circular_buf_t*, %struct.circular_buf_t** %4, align 8
  %179 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %178, i32 0, i32 1
  store i64 0, i64* %179, align 8
  %180 = load %struct.circular_buf_t*, %struct.circular_buf_t** %4, align 8
  %181 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %180, i32 0, i32 2
  store i64 0, i64* %181, align 8
  store i32 0, i32* %5, align 4
  br label %182

; <label>:182:                                    ; preds = %168, %177
  %183 = load i32, i32* %5, align 4
  store i32 -1, i32* %24, align 4
  br label %407

; <label>:184:                                    ; preds = %3
  %185 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %186 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %185, i32 0, i32 2
  %187 = load i8, i8* %186, align 2
  %188 = zext i8 %187 to i32
  %189 = load i32, i32* %29, align 4
  %190 = add nsw i32 %188, %189
  %191 = trunc i32 %190 to i8
  store i8 %191, i8* %30, align 1
  %192 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %193 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %192, i32 0, i32 5
  %194 = load i64*, i64** %193, align 8
  %195 = load i8, i8* %30, align 1
  %196 = zext i8 %195 to i64
  %197 = getelementptr inbounds i64, i64* %194, i64 %196
  %198 = load i64, i64* %197, align 8
  %199 = icmp eq i64 %198, 9223372036854775807
  br i1 %199, label %200, label %321

; <label>:200:                                    ; preds = %184
  %201 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %202 = load i64, i64* %26, align 8
  %203 = load i32, i32* %29, align 4
  %204 = trunc i32 %203 to i8
  store %struct.VCHN_t* %201, %struct.VCHN_t** %6, align 8
  store i64 %202, i64* %7, align 8
  store i8 %204, i8* %8, align 1
  %205 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %206 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %205, i32 0, i32 2
  %207 = load i8, i8* %206, align 2
  %208 = zext i8 %207 to i32
  %209 = load i8, i8* %8, align 1
  %210 = zext i8 %209 to i32
  %211 = add nsw i32 %208, %210
  %212 = trunc i32 %211 to i8
  store i8 %212, i8* %9, align 1
  %213 = load i64, i64* %7, align 8
  %214 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %215 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %214, i32 0, i32 5
  %216 = load i64*, i64** %215, align 8
  %217 = load i8, i8* %9, align 1
  %218 = zext i8 %217 to i64
  %219 = getelementptr inbounds i64, i64* %216, i64 %218
  store i64 %213, i64* %219, align 8
  %220 = load i8, i8* %8, align 1
  %221 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %222 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %221, i32 0, i32 6
  %223 = load i8*, i8** %222, align 8
  %224 = load i8, i8* %9, align 1
  %225 = zext i8 %224 to i64
  %226 = getelementptr inbounds i8, i8* %223, i64 %225
  store i8 %220, i8* %226, align 1
  br label %227

; <label>:227:                                    ; preds = %317, %200
  %228 = load i8, i8* %9, align 1
  %229 = zext i8 %228 to i32
  %230 = icmp sgt i32 %229, 0
  br i1 %230, label %231, label %319

; <label>:231:                                    ; preds = %227
  %232 = load i8, i8* %9, align 1
  %233 = zext i8 %232 to i32
  %234 = sub nsw i32 %233, 1
  %235 = sdiv i32 %234, 2
  %236 = trunc i32 %235 to i8
  store i8 %236, i8* %10, align 1
  %237 = load i8, i8* %10, align 1
  %238 = zext i8 %237 to i32
  %239 = add nsw i32 %238, 1
  %240 = mul nsw i32 %239, 2
  %241 = sub nsw i32 %240, 1
  %242 = trunc i32 %241 to i8
  store i8 %242, i8* %11, align 1
  %243 = load i8, i8* %10, align 1
  %244 = zext i8 %243 to i32
  %245 = add nsw i32 %244, 1
  %246 = mul nsw i32 %245, 2
  %247 = trunc i32 %246 to i8
  store i8 %247, i8* %12, align 1
  %248 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %249 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %248, i32 0, i32 5
  %250 = load i64*, i64** %249, align 8
  %251 = load i8, i8* %11, align 1
  %252 = zext i8 %251 to i64
  %253 = getelementptr inbounds i64, i64* %250, i64 %252
  %254 = load i64, i64* %253, align 8
  %255 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %256 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %255, i32 0, i32 5
  %257 = load i64*, i64** %256, align 8
  %258 = load i8, i8* %12, align 1
  %259 = zext i8 %258 to i64
  %260 = getelementptr inbounds i64, i64* %257, i64 %259
  %261 = load i64, i64* %260, align 8
  %262 = icmp slt i64 %254, %261
  br i1 %262, label %263, label %290

; <label>:263:                                    ; preds = %231
  %264 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %265 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %264, i32 0, i32 5
  %266 = load i64*, i64** %265, align 8
  %267 = load i8, i8* %11, align 1
  %268 = zext i8 %267 to i64
  %269 = getelementptr inbounds i64, i64* %266, i64 %268
  %270 = load i64, i64* %269, align 8
  %271 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %272 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %271, i32 0, i32 5
  %273 = load i64*, i64** %272, align 8
  %274 = load i8, i8* %10, align 1
  %275 = zext i8 %274 to i64
  %276 = getelementptr inbounds i64, i64* %273, i64 %275
  store i64 %270, i64* %276, align 8
  %277 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %278 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %277, i32 0, i32 6
  %279 = load i8*, i8** %278, align 8
  %280 = load i8, i8* %11, align 1
  %281 = zext i8 %280 to i64
  %282 = getelementptr inbounds i8, i8* %279, i64 %281
  %283 = load i8, i8* %282, align 1
  %284 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %285 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %284, i32 0, i32 6
  %286 = load i8*, i8** %285, align 8
  %287 = load i8, i8* %10, align 1
  %288 = zext i8 %287 to i64
  %289 = getelementptr inbounds i8, i8* %286, i64 %288
  store i8 %283, i8* %289, align 1
  br label %317

; <label>:290:                                    ; preds = %231
  %291 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %292 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %291, i32 0, i32 5
  %293 = load i64*, i64** %292, align 8
  %294 = load i8, i8* %12, align 1
  %295 = zext i8 %294 to i64
  %296 = getelementptr inbounds i64, i64* %293, i64 %295
  %297 = load i64, i64* %296, align 8
  %298 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %299 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %298, i32 0, i32 5
  %300 = load i64*, i64** %299, align 8
  %301 = load i8, i8* %10, align 1
  %302 = zext i8 %301 to i64
  %303 = getelementptr inbounds i64, i64* %300, i64 %302
  store i64 %297, i64* %303, align 8
  %304 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %305 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %304, i32 0, i32 6
  %306 = load i8*, i8** %305, align 8
  %307 = load i8, i8* %12, align 1
  %308 = zext i8 %307 to i64
  %309 = getelementptr inbounds i8, i8* %306, i64 %308
  %310 = load i8, i8* %309, align 1
  %311 = load %struct.VCHN_t*, %struct.VCHN_t** %6, align 8
  %312 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %311, i32 0, i32 6
  %313 = load i8*, i8** %312, align 8
  %314 = load i8, i8* %10, align 1
  %315 = zext i8 %314 to i64
  %316 = getelementptr inbounds i8, i8* %313, i64 %315
  store i8 %310, i8* %316, align 1
  br label %317

; <label>:317:                                    ; preds = %290, %263
  %318 = load i8, i8* %10, align 1
  store i8 %318, i8* %9, align 1
  br label %227

; <label>:319:                                    ; preds = %227
  store i32 0, i32* %31, align 4
  %320 = load i32, i32* %31, align 4
  store i32 %320, i32* %24, align 4
  br label %407

; <label>:321:                                    ; preds = %184
  %322 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %323 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %322, i32 0, i32 7
  %324 = load %struct.circular_buf_t*, %struct.circular_buf_t** %323, align 8
  %325 = load i32, i32* %28, align 4
  %326 = sext i32 %325 to i64
  %327 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %324, i64 %326
  %328 = bitcast %struct.circular_buf_t* %32 to i8*
  %329 = bitcast %struct.circular_buf_t* %327 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %328, i8* align 8 %329, i64 32, i1 false)
  %330 = bitcast %struct.circular_buf_t* %13 to i8*
  %331 = bitcast %struct.circular_buf_t* %32 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %330, i8* align 1 %331, i64 32, i1 false)
  %332 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %13, i32 0, i32 1
  %333 = load i64, i64* %332, align 8
  %334 = add nsw i64 %333, 1
  %335 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %13, i32 0, i32 3
  %336 = load i64, i64* %335, align 8
  %337 = srem i64 %334, %336
  %338 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %13, i32 0, i32 2
  %339 = load i64, i64* %338, align 8
  %340 = icmp eq i64 %337, %339
  br i1 %340, label %341, label %356

; <label>:341:                                    ; preds = %321
  %342 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %343 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %342, i32 0, i32 7
  %344 = load %struct.circular_buf_t*, %struct.circular_buf_t** %343, align 8
  %345 = load i32, i32* %28, align 4
  %346 = sext i32 %345 to i64
  %347 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %344, i64 %346
  %348 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %347, i32 0, i32 0
  %349 = load i64*, i64** %348, align 8
  %350 = ptrtoint i64* %349 to i64
  %351 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([34 x i8], [34 x i8]* @.str.8, i32 0, i32 0), i64 %350)
  %352 = sext i32 %351 to i64
  store i64 %352, i64* @controlflow_guarantee, align 8
  br label %353

; <label>:353:                                    ; preds = %341, %353
  %354 = load i64, i64* @controlflow_guarantee, align 8
  %355 = add nsw i64 %354, 1
  store i64 %355, i64* @controlflow_guarantee, align 8
  br label %353

; <label>:356:                                    ; preds = %321
  %357 = load %struct.VCHN_t*, %struct.VCHN_t** %25, align 8
  %358 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %357, i32 0, i32 7
  %359 = load %struct.circular_buf_t*, %struct.circular_buf_t** %358, align 8
  %360 = load i32, i32* %28, align 4
  %361 = sext i32 %360 to i64
  %362 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %359, i64 %361
  %363 = load i64, i64* %26, align 8
  store %struct.circular_buf_t* %362, %struct.circular_buf_t** %14, align 8
  store i64 %363, i64* %15, align 8
  store i32 -1, i32* %16, align 4
  %364 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %365 = icmp ne %struct.circular_buf_t* %364, null
  br i1 %365, label %366, label %404

; <label>:366:                                    ; preds = %356
  %367 = load i64, i64* %15, align 8
  %368 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %369 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %368, i32 0, i32 0
  %370 = load i64*, i64** %369, align 8
  %371 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %372 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %371, i32 0, i32 1
  %373 = load i64, i64* %372, align 8
  %374 = getelementptr inbounds i64, i64* %370, i64 %373
  store i64 %367, i64* %374, align 8
  %375 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %376 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %375, i32 0, i32 1
  %377 = load i64, i64* %376, align 8
  %378 = add nsw i64 %377, 1
  %379 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %380 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %379, i32 0, i32 3
  %381 = load i64, i64* %380, align 8
  %382 = srem i64 %378, %381
  %383 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %384 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %383, i32 0, i32 1
  store i64 %382, i64* %384, align 8
  %385 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %386 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %385, i32 0, i32 1
  %387 = load i64, i64* %386, align 8
  %388 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %389 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %388, i32 0, i32 2
  %390 = load i64, i64* %389, align 8
  %391 = icmp eq i64 %387, %390
  br i1 %391, label %392, label %403

; <label>:392:                                    ; preds = %366
  %393 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %394 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %393, i32 0, i32 2
  %395 = load i64, i64* %394, align 8
  %396 = add nsw i64 %395, 1
  %397 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %398 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %397, i32 0, i32 3
  %399 = load i64, i64* %398, align 8
  %400 = srem i64 %396, %399
  %401 = load %struct.circular_buf_t*, %struct.circular_buf_t** %14, align 8
  %402 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %401, i32 0, i32 2
  store i64 %400, i64* %402, align 8
  br label %403

; <label>:403:                                    ; preds = %392, %366
  store i32 0, i32* %16, align 4
  br label %404

; <label>:404:                                    ; preds = %356, %403
  %405 = load i32, i32* %16, align 4
  store i32 %405, i32* %33, align 4
  %406 = load i32, i32* %33, align 4
  store i32 %406, i32* %24, align 4
  br label %407

; <label>:407:                                    ; preds = %404, %319, %182
  %408 = load i32, i32* %24, align 4
  ret i32 %408
}

; Function Attrs: alwaysinline uwtable
define dso_local i64 @VCHN_next(%struct.VCHN_t*, i8*) #1 {
  %3 = alloca %struct.VCHN_t*, align 8
  %4 = alloca i64, align 8
  %5 = alloca i8, align 1
  %6 = alloca i8, align 1
  %7 = alloca i8, align 1
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca %struct.circular_buf_t, align 8
  %11 = alloca %struct.circular_buf_t*, align 8
  %12 = alloca i64*, align 8
  %13 = alloca i8, align 1
  %14 = alloca i32, align 4
  %15 = alloca %struct.circular_buf_t, align 8
  %16 = alloca %struct.VCHN_t*, align 8
  %17 = alloca i64, align 8
  %18 = alloca i8, align 1
  %19 = alloca i8, align 1
  %20 = alloca i8, align 1
  %21 = alloca i8, align 1
  %22 = alloca i8, align 1
  %23 = alloca %struct.circular_buf_t, align 8
  %24 = alloca %struct.VCHN_t*, align 8
  %25 = alloca i8*, align 8
  %26 = alloca i64, align 8
  %27 = alloca i8, align 1
  %28 = alloca i32, align 4
  %29 = alloca %struct.circular_buf_t, align 8
  %30 = alloca i64, align 8
  store %struct.VCHN_t* %0, %struct.VCHN_t** %24, align 8
  store i8* %1, i8** %25, align 8
  %31 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %32 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %31, i32 0, i32 5
  %33 = load i64*, i64** %32, align 8
  %34 = getelementptr inbounds i64, i64* %33, i64 0
  %35 = load i64, i64* %34, align 8
  store i64 %35, i64* %26, align 8
  %36 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %37 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %36, i32 0, i32 6
  %38 = load i8*, i8** %37, align 8
  %39 = getelementptr inbounds i8, i8* %38, i64 0
  %40 = load i8, i8* %39, align 1
  store i8 %40, i8* %27, align 1
  %41 = load i8, i8* %27, align 1
  %42 = zext i8 %41 to i32
  %43 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %44 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %43, i32 0, i32 1
  %45 = load i8, i8* %44, align 1
  %46 = zext i8 %45 to i32
  %47 = sub nsw i32 %42, %46
  store i32 %47, i32* %28, align 4
  %48 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %49 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %48, i32 0, i32 0
  %50 = load i8, i8* %49, align 8
  %51 = zext i8 %50 to i32
  %52 = load i32, i32* %28, align 4
  %53 = add nsw i32 %51, %52
  %54 = trunc i32 %53 to i8
  %55 = load i8*, i8** %25, align 8
  store i8 %54, i8* %55, align 1
  %56 = load i64, i64* %26, align 8
  %57 = icmp slt i64 %56, 9223372036854775807
  br i1 %57, label %58, label %364

; <label>:58:                                     ; preds = %2
  %59 = load i32, i32* %28, align 4
  %60 = icmp sge i32 %59, 0
  br i1 %60, label %61, label %363

; <label>:61:                                     ; preds = %58
  %62 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %63 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %62, i32 0, i32 7
  %64 = load %struct.circular_buf_t*, %struct.circular_buf_t** %63, align 8
  %65 = load i32, i32* %28, align 4
  %66 = sext i32 %65 to i64
  %67 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %64, i64 %66
  %68 = bitcast %struct.circular_buf_t* %29 to i8*
  %69 = bitcast %struct.circular_buf_t* %67 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %68, i8* align 8 %69, i64 32, i1 false)
  %70 = bitcast %struct.circular_buf_t* %23 to i8*
  %71 = bitcast %struct.circular_buf_t* %29 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %70, i8* align 1 %71, i64 32, i1 false)
  %72 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %23, i32 0, i32 1
  %73 = load i64, i64* %72, align 8
  %74 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %23, i32 0, i32 2
  %75 = load i64, i64* %74, align 8
  %76 = icmp eq i64 %73, %75
  br i1 %76, label %77, label %195

; <label>:77:                                     ; preds = %61
  %78 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %79 = load i8, i8* %27, align 1
  store %struct.VCHN_t* %78, %struct.VCHN_t** %3, align 8
  store i64 9223372036854775807, i64* %4, align 8
  store i8 %79, i8* %5, align 1
  %80 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %81 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %80, i32 0, i32 2
  %82 = load i8, i8* %81, align 2
  %83 = zext i8 %82 to i32
  %84 = load i8, i8* %5, align 1
  %85 = zext i8 %84 to i32
  %86 = add nsw i32 %83, %85
  %87 = trunc i32 %86 to i8
  store i8 %87, i8* %6, align 1
  %88 = load i64, i64* %4, align 8
  %89 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %90 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %89, i32 0, i32 5
  %91 = load i64*, i64** %90, align 8
  %92 = load i8, i8* %6, align 1
  %93 = zext i8 %92 to i64
  %94 = getelementptr inbounds i64, i64* %91, i64 %93
  store i64 %88, i64* %94, align 8
  %95 = load i8, i8* %5, align 1
  %96 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %97 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %96, i32 0, i32 6
  %98 = load i8*, i8** %97, align 8
  %99 = load i8, i8* %6, align 1
  %100 = zext i8 %99 to i64
  %101 = getelementptr inbounds i8, i8* %98, i64 %100
  store i8 %95, i8* %101, align 1
  br label %102

; <label>:102:                                    ; preds = %192, %77
  %103 = load i8, i8* %6, align 1
  %104 = zext i8 %103 to i32
  %105 = icmp sgt i32 %104, 0
  br i1 %105, label %106, label %194

; <label>:106:                                    ; preds = %102
  %107 = load i8, i8* %6, align 1
  %108 = zext i8 %107 to i32
  %109 = sub nsw i32 %108, 1
  %110 = sdiv i32 %109, 2
  %111 = trunc i32 %110 to i8
  store i8 %111, i8* %7, align 1
  %112 = load i8, i8* %7, align 1
  %113 = zext i8 %112 to i32
  %114 = add nsw i32 %113, 1
  %115 = mul nsw i32 %114, 2
  %116 = sub nsw i32 %115, 1
  %117 = trunc i32 %116 to i8
  store i8 %117, i8* %8, align 1
  %118 = load i8, i8* %7, align 1
  %119 = zext i8 %118 to i32
  %120 = add nsw i32 %119, 1
  %121 = mul nsw i32 %120, 2
  %122 = trunc i32 %121 to i8
  store i8 %122, i8* %9, align 1
  %123 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %124 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %123, i32 0, i32 5
  %125 = load i64*, i64** %124, align 8
  %126 = load i8, i8* %8, align 1
  %127 = zext i8 %126 to i64
  %128 = getelementptr inbounds i64, i64* %125, i64 %127
  %129 = load i64, i64* %128, align 8
  %130 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %131 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %130, i32 0, i32 5
  %132 = load i64*, i64** %131, align 8
  %133 = load i8, i8* %9, align 1
  %134 = zext i8 %133 to i64
  %135 = getelementptr inbounds i64, i64* %132, i64 %134
  %136 = load i64, i64* %135, align 8
  %137 = icmp slt i64 %129, %136
  br i1 %137, label %138, label %165

; <label>:138:                                    ; preds = %106
  %139 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %140 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %139, i32 0, i32 5
  %141 = load i64*, i64** %140, align 8
  %142 = load i8, i8* %8, align 1
  %143 = zext i8 %142 to i64
  %144 = getelementptr inbounds i64, i64* %141, i64 %143
  %145 = load i64, i64* %144, align 8
  %146 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %147 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %146, i32 0, i32 5
  %148 = load i64*, i64** %147, align 8
  %149 = load i8, i8* %7, align 1
  %150 = zext i8 %149 to i64
  %151 = getelementptr inbounds i64, i64* %148, i64 %150
  store i64 %145, i64* %151, align 8
  %152 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %153 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %152, i32 0, i32 6
  %154 = load i8*, i8** %153, align 8
  %155 = load i8, i8* %8, align 1
  %156 = zext i8 %155 to i64
  %157 = getelementptr inbounds i8, i8* %154, i64 %156
  %158 = load i8, i8* %157, align 1
  %159 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %160 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %159, i32 0, i32 6
  %161 = load i8*, i8** %160, align 8
  %162 = load i8, i8* %7, align 1
  %163 = zext i8 %162 to i64
  %164 = getelementptr inbounds i8, i8* %161, i64 %163
  store i8 %158, i8* %164, align 1
  br label %192

; <label>:165:                                    ; preds = %106
  %166 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %167 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %166, i32 0, i32 5
  %168 = load i64*, i64** %167, align 8
  %169 = load i8, i8* %9, align 1
  %170 = zext i8 %169 to i64
  %171 = getelementptr inbounds i64, i64* %168, i64 %170
  %172 = load i64, i64* %171, align 8
  %173 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %174 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %173, i32 0, i32 5
  %175 = load i64*, i64** %174, align 8
  %176 = load i8, i8* %7, align 1
  %177 = zext i8 %176 to i64
  %178 = getelementptr inbounds i64, i64* %175, i64 %177
  store i64 %172, i64* %178, align 8
  %179 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %180 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %179, i32 0, i32 6
  %181 = load i8*, i8** %180, align 8
  %182 = load i8, i8* %9, align 1
  %183 = zext i8 %182 to i64
  %184 = getelementptr inbounds i8, i8* %181, i64 %183
  %185 = load i8, i8* %184, align 1
  %186 = load %struct.VCHN_t*, %struct.VCHN_t** %3, align 8
  %187 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %186, i32 0, i32 6
  %188 = load i8*, i8** %187, align 8
  %189 = load i8, i8* %7, align 1
  %190 = zext i8 %189 to i64
  %191 = getelementptr inbounds i8, i8* %188, i64 %190
  store i8 %185, i8* %191, align 1
  br label %192

; <label>:192:                                    ; preds = %165, %138
  %193 = load i8, i8* %7, align 1
  store i8 %193, i8* %6, align 1
  br label %102

; <label>:194:                                    ; preds = %102
  br label %362

; <label>:195:                                    ; preds = %61
  %196 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %197 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %196, i32 0, i32 7
  %198 = load %struct.circular_buf_t*, %struct.circular_buf_t** %197, align 8
  %199 = load i32, i32* %28, align 4
  %200 = sext i32 %199 to i64
  %201 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %198, i64 %200
  store %struct.circular_buf_t* %201, %struct.circular_buf_t** %11, align 8
  store i64* %30, i64** %12, align 8
  store i8 1, i8* %13, align 1
  store i32 -1, i32* %14, align 4
  %202 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %203 = icmp ne %struct.circular_buf_t* %202, null
  br i1 %203, label %204, label %242

; <label>:204:                                    ; preds = %195
  %205 = load i64*, i64** %12, align 8
  %206 = icmp ne i64* %205, null
  br i1 %206, label %207, label %242

; <label>:207:                                    ; preds = %204
  %208 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %209 = bitcast %struct.circular_buf_t* %15 to i8*
  %210 = bitcast %struct.circular_buf_t* %208 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %209, i8* align 8 %210, i64 32, i1 false)
  %211 = bitcast %struct.circular_buf_t* %10 to i8*
  %212 = bitcast %struct.circular_buf_t* %15 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %211, i8* align 1 %212, i64 32, i1 false)
  %213 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %10, i32 0, i32 1
  %214 = load i64, i64* %213, align 8
  %215 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %10, i32 0, i32 2
  %216 = load i64, i64* %215, align 8
  %217 = icmp eq i64 %214, %216
  br i1 %217, label %242, label %218

; <label>:218:                                    ; preds = %207
  %219 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %220 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %219, i32 0, i32 0
  %221 = load i64*, i64** %220, align 8
  %222 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %223 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %222, i32 0, i32 2
  %224 = load i64, i64* %223, align 8
  %225 = getelementptr inbounds i64, i64* %221, i64 %224
  %226 = load i64, i64* %225, align 8
  %227 = load i64*, i64** %12, align 8
  store i64 %226, i64* %227, align 8
  %228 = load i8, i8* %13, align 1
  %229 = trunc i8 %228 to i1
  br i1 %229, label %230, label %241

; <label>:230:                                    ; preds = %218
  %231 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %232 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %231, i32 0, i32 2
  %233 = load i64, i64* %232, align 8
  %234 = add nsw i64 %233, 1
  %235 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %236 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %235, i32 0, i32 3
  %237 = load i64, i64* %236, align 8
  %238 = srem i64 %234, %237
  %239 = load %struct.circular_buf_t*, %struct.circular_buf_t** %11, align 8
  %240 = getelementptr inbounds %struct.circular_buf_t, %struct.circular_buf_t* %239, i32 0, i32 2
  store i64 %238, i64* %240, align 8
  br label %241

; <label>:241:                                    ; preds = %230, %218
  store i32 0, i32* %14, align 4
  br label %242

; <label>:242:                                    ; preds = %195, %204, %207, %241
  %243 = load i32, i32* %14, align 4
  %244 = load %struct.VCHN_t*, %struct.VCHN_t** %24, align 8
  %245 = load i64, i64* %30, align 8
  %246 = load i8, i8* %27, align 1
  store %struct.VCHN_t* %244, %struct.VCHN_t** %16, align 8
  store i64 %245, i64* %17, align 8
  store i8 %246, i8* %18, align 1
  %247 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %248 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %247, i32 0, i32 2
  %249 = load i8, i8* %248, align 2
  %250 = zext i8 %249 to i32
  %251 = load i8, i8* %18, align 1
  %252 = zext i8 %251 to i32
  %253 = add nsw i32 %250, %252
  %254 = trunc i32 %253 to i8
  store i8 %254, i8* %19, align 1
  %255 = load i64, i64* %17, align 8
  %256 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %257 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %256, i32 0, i32 5
  %258 = load i64*, i64** %257, align 8
  %259 = load i8, i8* %19, align 1
  %260 = zext i8 %259 to i64
  %261 = getelementptr inbounds i64, i64* %258, i64 %260
  store i64 %255, i64* %261, align 8
  %262 = load i8, i8* %18, align 1
  %263 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %264 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %263, i32 0, i32 6
  %265 = load i8*, i8** %264, align 8
  %266 = load i8, i8* %19, align 1
  %267 = zext i8 %266 to i64
  %268 = getelementptr inbounds i8, i8* %265, i64 %267
  store i8 %262, i8* %268, align 1
  br label %269

; <label>:269:                                    ; preds = %359, %242
  %270 = load i8, i8* %19, align 1
  %271 = zext i8 %270 to i32
  %272 = icmp sgt i32 %271, 0
  br i1 %272, label %273, label %361

; <label>:273:                                    ; preds = %269
  %274 = load i8, i8* %19, align 1
  %275 = zext i8 %274 to i32
  %276 = sub nsw i32 %275, 1
  %277 = sdiv i32 %276, 2
  %278 = trunc i32 %277 to i8
  store i8 %278, i8* %20, align 1
  %279 = load i8, i8* %20, align 1
  %280 = zext i8 %279 to i32
  %281 = add nsw i32 %280, 1
  %282 = mul nsw i32 %281, 2
  %283 = sub nsw i32 %282, 1
  %284 = trunc i32 %283 to i8
  store i8 %284, i8* %21, align 1
  %285 = load i8, i8* %20, align 1
  %286 = zext i8 %285 to i32
  %287 = add nsw i32 %286, 1
  %288 = mul nsw i32 %287, 2
  %289 = trunc i32 %288 to i8
  store i8 %289, i8* %22, align 1
  %290 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %291 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %290, i32 0, i32 5
  %292 = load i64*, i64** %291, align 8
  %293 = load i8, i8* %21, align 1
  %294 = zext i8 %293 to i64
  %295 = getelementptr inbounds i64, i64* %292, i64 %294
  %296 = load i64, i64* %295, align 8
  %297 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %298 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %297, i32 0, i32 5
  %299 = load i64*, i64** %298, align 8
  %300 = load i8, i8* %22, align 1
  %301 = zext i8 %300 to i64
  %302 = getelementptr inbounds i64, i64* %299, i64 %301
  %303 = load i64, i64* %302, align 8
  %304 = icmp slt i64 %296, %303
  br i1 %304, label %305, label %332

; <label>:305:                                    ; preds = %273
  %306 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %307 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %306, i32 0, i32 5
  %308 = load i64*, i64** %307, align 8
  %309 = load i8, i8* %21, align 1
  %310 = zext i8 %309 to i64
  %311 = getelementptr inbounds i64, i64* %308, i64 %310
  %312 = load i64, i64* %311, align 8
  %313 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %314 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %313, i32 0, i32 5
  %315 = load i64*, i64** %314, align 8
  %316 = load i8, i8* %20, align 1
  %317 = zext i8 %316 to i64
  %318 = getelementptr inbounds i64, i64* %315, i64 %317
  store i64 %312, i64* %318, align 8
  %319 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %320 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %319, i32 0, i32 6
  %321 = load i8*, i8** %320, align 8
  %322 = load i8, i8* %21, align 1
  %323 = zext i8 %322 to i64
  %324 = getelementptr inbounds i8, i8* %321, i64 %323
  %325 = load i8, i8* %324, align 1
  %326 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %327 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %326, i32 0, i32 6
  %328 = load i8*, i8** %327, align 8
  %329 = load i8, i8* %20, align 1
  %330 = zext i8 %329 to i64
  %331 = getelementptr inbounds i8, i8* %328, i64 %330
  store i8 %325, i8* %331, align 1
  br label %359

; <label>:332:                                    ; preds = %273
  %333 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %334 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %333, i32 0, i32 5
  %335 = load i64*, i64** %334, align 8
  %336 = load i8, i8* %22, align 1
  %337 = zext i8 %336 to i64
  %338 = getelementptr inbounds i64, i64* %335, i64 %337
  %339 = load i64, i64* %338, align 8
  %340 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %341 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %340, i32 0, i32 5
  %342 = load i64*, i64** %341, align 8
  %343 = load i8, i8* %20, align 1
  %344 = zext i8 %343 to i64
  %345 = getelementptr inbounds i64, i64* %342, i64 %344
  store i64 %339, i64* %345, align 8
  %346 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %347 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %346, i32 0, i32 6
  %348 = load i8*, i8** %347, align 8
  %349 = load i8, i8* %22, align 1
  %350 = zext i8 %349 to i64
  %351 = getelementptr inbounds i8, i8* %348, i64 %350
  %352 = load i8, i8* %351, align 1
  %353 = load %struct.VCHN_t*, %struct.VCHN_t** %16, align 8
  %354 = getelementptr inbounds %struct.VCHN_t, %struct.VCHN_t* %353, i32 0, i32 6
  %355 = load i8*, i8** %354, align 8
  %356 = load i8, i8* %20, align 1
  %357 = zext i8 %356 to i64
  %358 = getelementptr inbounds i8, i8* %355, i64 %357
  store i8 %352, i8* %358, align 1
  br label %359

; <label>:359:                                    ; preds = %332, %305
  %360 = load i8, i8* %20, align 1
  store i8 %360, i8* %19, align 1
  br label %269

; <label>:361:                                    ; preds = %269
  br label %362

; <label>:362:                                    ; preds = %361, %194
  br label %363

; <label>:363:                                    ; preds = %362, %58
  br label %364

; <label>:364:                                    ; preds = %363, %2
  %365 = load i64, i64* %26, align 8
  ret i64 %365
}

attributes #0 = { alwaysinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { alwaysinline uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { argmemonly nounwind }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-3build1 (tags/RELEASE_801/final)"}
