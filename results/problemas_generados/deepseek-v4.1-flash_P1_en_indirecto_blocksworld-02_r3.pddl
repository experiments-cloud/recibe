(define (problem blocksworld-a-b-c-d)
  (:domain blocks)
  (:objects
    a b c d - block
  )
  (:init
    (on c b)
    (ontable a)
    (ontable b)
    (ontable d)
    (clear a)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
