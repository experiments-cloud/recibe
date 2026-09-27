(define (problem blocksworld-dcba)
  (:domain blocks)
  (:objects
    a b c d - block
  )
  (:init
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (handempty)
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
  )
  (:goal (and
    (on b a)
    (on c b)
    (on d c)
  ))
)
